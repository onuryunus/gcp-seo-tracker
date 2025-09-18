import json
import asyncio
import os
from typing import Dict, Any, AsyncIterable, Iterable, Union

from dotenv import load_dotenv

from google.genai.types import Part, Content
from google.adk.runners import InMemoryRunner
from google.adk.agents.run_config import RunConfig
from google.genai import types

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import logging
from starlette.websockets import WebSocketDisconnect

# Import the root agent from the app directory
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.agent import root_agent

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="PubTender API", description="SEO Analysis API with Google ADK")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections
active_connections: Dict[str, Dict[str, Any]] = {}

# Create a single runner at process start (opsiyonel ama pratik)
RUNNER = InMemoryRunner(
    app_name=os.getenv("APP_NAME", "pubtender"),
    agent=root_agent
)

async def start_session_for_user(user_id: str):
    """Create (or reuse) a session for this user (non-live)."""
    try:
        session = await RUNNER.session_service.create_session(
            app_name=os.getenv("APP_NAME", "pubtender"),
            user_id=user_id,
        )
        logger.info(f"Session started for user {user_id}")
        return session
    except Exception as e:
        logger.error(f"Error starting session for user {user_id}: {e}")
        raise

def _extract_text_from_event_content(content: Content) -> str:
    if not content or not getattr(content, "parts", None):
        return ""
    return "".join(p.text for p in content.parts if getattr(p, "text", None))

async def _run_single_turn(session, user_text: str) -> str:
    """
    Run a single non-streaming turn and return the model's text output.
    This handles both iterable events and direct result objects.
    """
    # Non-live RunConfig (no streaming_mode)
    run_config = RunConfig(
        # session_resumption=types.SessionResumptionConfig(transparent=True),
        response_modalities=["TEXT"],
    )

    user_content = Content(role="user", parts=[Part.from_text(text=user_text)])

    # Çalıştır - session.id kullan, session.user_id değil
    result = RUNNER.run(
        session_id=session.id,
        new_message=user_content,
        run_config=run_config,
        user_id=session.user_id
    )

    # Sonuç iterable ise (bazı ADK sürümleri event stream değil de iterable döndürebilir)
    if isinstance(result, (AsyncIterable,)):
        out = []
        async for event in result:  # type: ignore
            # Event model cevabı ise topla
            if getattr(event, "content", None) and getattr(event.content, "role", None) == "model":
                out.append(_extract_text_from_event_content(event.content))
        return "".join(out).strip()

    # Sync iterable?
    if isinstance(result, Iterable):
        out = []
        for event in result:  # type: ignore
            if getattr(event, "content", None) and getattr(event.content, "role", None) == "model":
                out.append(_extract_text_from_event_content(event.content))
        if out:
            return "".join(out).strip()

    # RunResult benzeri bir obje ise, muhtemelen `.response`/`.content` barındırır
    # Aşağıdaki blok farklı ADK versiyonlarını kibarca normalize eder:
    for attr in ("response", "content", "contents", "result"):
        if hasattr(result, attr):
            val = getattr(result, attr)
            # Tek Content
            if isinstance(val, Content):
                return _extract_text_from_event_content(val).strip()
            # Liste
            if isinstance(val, (list, tuple)) and val and isinstance(val[0], Content):
                text_parts = [_extract_text_from_event_content(c) for c in val]
                return "".join(text_parts).strip()

    # Son çare: stringe çevir
    return str(result)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Client websocket endpoint (non-live; her mesaj için tek run)."""
    logger.info(f"WebSocket connection attempt from user {user_id}")
    await websocket.accept()
    logger.info(f"WebSocket connection accepted for user {user_id}")

    try:
        session = await start_session_for_user(user_id)
        active_connections[user_id] = {
            "websocket": websocket,
            "session": session
        }

        while True:
            try:
                message_json = await websocket.receive_text()
                message = json.loads(message_json)
                mime_type = message.get("mime_type", "text/plain")

                if mime_type != "text/plain":
                    logger.warning(f"Unsupported mime type from user {user_id}: {mime_type}")
                    await websocket.send_text(json.dumps({
                        "author": "system",
                        "is_partial": False,
                        "turn_complete": True,
                        "parts": [{"type": "text", "data": f"Unsupported mime type: {mime_type}"}],
                    }))
                    continue

                user_text = message.get("data", "")
                logger.info(f"Received text from user {user_id}: {user_text[:80]}...")

                # Tek-istek/tek-cevap çalıştır
                try:
                    model_text = await _run_single_turn(session, user_text)
                except Exception as run_err:
                    logger.error(f"Run error for user {user_id}: {run_err}")
                    model_text = f"Error while running analysis: {run_err}"

                # Tek cevap gönder
                await websocket.send_text(json.dumps({
                    "author": "agent",
                    "is_partial": False,
                    "turn_complete": True,
                    "interrupted": False,
                    "parts": [{"type": "text", "data": model_text}],
                    "input_transcription": {"text": user_text, "is_final": True},
                    "output_transcription": {"text": model_text, "is_final": True}
                }))

            except WebSocketDisconnect:
                logger.info(f"Client {user_id} disconnected (WebSocketDisconnect).")
                break
            except Exception as e:
                logger.error(f"Error in websocket loop for user {user_id}: {e}")
                break

    except Exception as e:
        logger.error(f"Error in websocket_endpoint for user {user_id}: {e}")

    finally:
        if user_id in active_connections:
            del active_connections[user_id]
        logger.info(f"Client {user_id} disconnected and cleaned up")

@app.post("/analyze")
async def analyze(payload: Dict[str, Any]):
    """
    Basit HTTP endpoint: body = {"user_id": "...", "text": "..."}
    Live yok; tek run çalışır.
    """
    user_id = payload.get("user_id") or "anonymous"
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text'")

    try:
        session = await start_session_for_user(user_id)
        model_text = await _run_single_turn(session, text)
        return {"user_id": user_id, "text": text, "response": model_text}
    except Exception as e:
        logger.error(f"/analyze error for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "active_connections": len(active_connections)}

@app.get("/")
async def root():
    return {
        "message": "PubTender SEO Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "websocket": "/ws/{user_id}",
            "analyze": "/analyze",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
