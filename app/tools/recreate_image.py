import os
from typing import Dict, Any
from dotenv import load_dotenv
import google.genai as genai

from google.adk.tools.tool_context import ToolContext

IMAGE_MODEL = "gemini-2.5-flash"

async def generate_custom_image(
        tool_context: ToolContext,
        prompt: str = "",
        output_filename: str = "custom_image.png"
) -> Dict[str, Any]:
    """
    Generates a detailed image description based on a custom text prompt using Gemini API.

    Args:
        tool_context: ADK tool context
        prompt: Text prompt for image generation
        output_filename: Name of the output image file (for reference)

    Returns:
        Image description results
    """
    if not prompt:
        return {
            "status": "error",
            "message": "Prompt parameter is required for custom image generation"
        }

    # Configure Gemini API
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "message": "GOOGLE_API_KEY or GEMINI_API_KEY environment variable is required"
        }

    try:
        genai.configure(api_key=api_key)

        # Use Gemini to create detailed image description
        model = genai.GenerativeModel(IMAGE_MODEL)

        # Generate a detailed image description using Gemini
        description_prompt = f"""
        Create a detailed visual description for an image based on this prompt: "{prompt}"

        Provide a comprehensive description that includes:
        - Main subject and focal points
        - Visual style and artistic approach
        - Color palette and lighting
        - Composition and layout
        - Background and environment
        - Mood and atmosphere
        - Technical details (if applicable)

        Make the description detailed enough that an artist or image generation tool could create the image accurately.
        """

        response = model.generate_content(description_prompt)
        image_description = response.text

        return {
            "status": "success",
            "message": f"Custom image description generated successfully",
            "image_description": image_description,
            "original_prompt": prompt,
            "suggested_filename": output_filename,
            "note": "This is a detailed text description for the image. You can use this description with image generation tools like DALL-E, Midjourney, or Stable Diffusion."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during custom image description generation: {str(e)}"
        }
