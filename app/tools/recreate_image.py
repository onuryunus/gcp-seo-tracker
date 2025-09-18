import os
from typing import Dict, Any
import google.genai as genai
from google.genai import Client, types

from google.adk.tools.tool_context import ToolContext

IMAGE_MODEL = "gemini-2.5-flash"

MODEL = "gemini-2.5-pro"

client = Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)

async def generate_image_with_alt_text(img_prompt: str, tool_context: ToolContext):
    """Generates an image based on the prompt using Vertex AI and creates SEO-optimized alt text."""
    try:
        response = client.models.generate_images(
            model=IMAGE_MODEL,
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

