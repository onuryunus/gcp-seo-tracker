# Copyright 2025 Google LLC
# Apache 2.0

"""Image Generator agent: Creates images from web content using Vertex AI"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import ToolContext, load_artifacts
from google.genai import Client, types

from . import prompt
from ...utils.web_crawler import crawl_webpage

MODEL = "gemini-2.5-pro"
MODEL_IMAGE = "imagen-3.0-generate-002"

load_dotenv()

client = Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)


async def generate_image_with_alt_text(img_prompt: str, tool_context: ToolContext):
    """Generates an image based on the prompt using Vertex AI and creates SEO-optimized alt text."""
    try:
        response = client.models.generate_images(
            model=MODEL_IMAGE,
            prompt=img_prompt,
            config={"number_of_images": 1},
        )
        if not response.generated_images:
            return {"status": "failed", "message": "No images were generated"}
        
        image_bytes = response.generated_images[0].image.image_bytes
        await tool_context.save_artifact(
            "generated_image.png",
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        )
        
        from google.genai import Client as GeminiClient
        
        gemini_client = GeminiClient(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        )
        
        alt_text_prompt = f"""
        Create a concise, SEO-optimized alt text for an image that was generated with this prompt: "{img_prompt}"
        
        The alt text should be:
        - Descriptive but concise (under 125 characters)
        - SEO-friendly with relevant keywords
        - Accessible for screen readers
        - Professional and clear
        
        Return only the alt text, nothing else.
        """
        
        alt_response = gemini_client.models.generate_content(
            model=MODEL,
            contents=alt_text_prompt
        )
        
        alt_text = alt_response.candidates[0].content.parts[0].text.strip()
        
        return {
            "status": "success",
            "detail": "Image generated successfully and stored in artifacts.",
            "filename": "generated_image.png",
            "prompt_used": img_prompt,
            "alt_text": alt_text,
            "seo_optimized": True
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during image generation: {str(e)}"
        }


async def generate_alt_text_for_web_images(
    tool_context: ToolContext,
    url: str = ""
) -> Dict[str, Any]:
    """
    Analyzes web page images and generates SEO-optimized alt texts.
    
    Args:
        tool_context: ADK tool context
        url: URL of the web page to analyze
        
    Returns:
        Alt text suggestions for web page images
    """
    if not url:
        return {
            "status": "error",
            "message": "URL parameter is required"
        }
    
    try:
        crawl_data = crawl_webpage(url)
        
        if 'error' in crawl_data:
            return {
                "status": "error",
                "message": f"Error crawling web page: {crawl_data['error']}",
                "url": url
            }
        
        images = crawl_data.get('images', [])
        if not images:
            return {
                "status": "success",
                "message": "No images found on the webpage",
                "url": url,
                "alt_text_suggestions": []
            }
        
        page_title = crawl_data.get('title', '')
        page_description = crawl_data.get('meta_description', '')
        keywords = crawl_data.get('keywords', [])[:10]
        page_context = f"Page: {page_title}. Description: {page_description}. Keywords: {', '.join(keywords)}"
        
        from google.genai import Client as GeminiClient
        
        gemini_client = GeminiClient(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        )
        
        alt_text_suggestions = []
        
        for i, img in enumerate(images[:10]):
            img_src = img.get('src', '')
            existing_alt = img.get('alt', '')
            
            alt_text_prompt = f"""
            Generate a SEO-optimized alt text for an image on this webpage.
            
            Page Context: {page_context}
            Image Source: {img_src}
            Current Alt Text: "{existing_alt}" (empty if none)
            
            Create an alt text that is:
            - Descriptive and relevant to the page content
            - SEO-optimized with page keywords when appropriate
            - Under 125 characters
            - Professional and accessible
            - Better than the existing alt text if one exists
            
            Return only the alt text, nothing else.
            """
            
            try:
                alt_response = gemini_client.models.generate_content(
                    model=MODEL,
                    contents=alt_text_prompt
                )
                
                suggested_alt = alt_response.candidates[0].content.parts[0].text.strip()
                
                alt_text_suggestions.append({
                    "image_index": i + 1,
                    "image_src": img_src,
                    "current_alt": existing_alt,
                    "suggested_alt": suggested_alt,
                    "improvement_needed": len(existing_alt.strip()) == 0 or len(suggested_alt) > len(existing_alt)
                })
                
            except Exception as e:
                alt_text_suggestions.append({
                    "image_index": i + 1,
                    "image_src": img_src,
                    "current_alt": existing_alt,
                    "error": f"Could not generate alt text: {str(e)}"
                })
        
        return {
            "status": "success",
            "url": url,
            "total_images": len(images),
            "processed_images": len(alt_text_suggestions),
            "alt_text_suggestions": alt_text_suggestions,
            "page_context": page_context
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during alt text generation: {str(e)}",
            "url": url
        }


image_generator_agent = Agent(
    model=MODEL,
    name="image_generator_agent",
    description=(
        "Generates high-quality images from web content or custom prompts using Vertex AI Imagen. "
        "Can analyze web page content and create relevant visuals, generate custom images from text descriptions, "
        "and create SEO-optimized alt texts for both generated and existing web page images."
    ),
    instruction=prompt.IMAGE_GENERATOR_PROMPT,
    output_key="image_generator_output",
    tools=[generate_image_with_alt_text, generate_alt_text_for_web_images, load_artifacts]
)
