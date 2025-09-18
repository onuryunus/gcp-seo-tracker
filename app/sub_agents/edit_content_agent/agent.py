from dotenv import load_dotenv

from google.adk import Agent
from app.tools.recreate_page import optimize_headings, optimize_title_tag, optimize_meta_description, optimize_paragraph_content, generate_image_alt_texts

from . import prompt
from app.tools.recreate_image import generate_image_with_alt_text

MODEL = "gemini-2.5-pro"
load_dotenv()

image_generator_agent = Agent(
    model=MODEL,
    name="image_generator_agent",
    description=(
        "Creates detailed image descriptions from web content or custom prompts using Gemini API. "
        "Can analyze web page content and generate professional image descriptions, or create custom image descriptions from text prompts."
    ),
    instruction=prompt.IMAGE_GENERATOR_PROMPT,
    output_key="image_generator_output",
    tools=[generate_image_with_alt_text]
)


edit_text_content_agent = Agent(
    model=MODEL,
    name="edit_text_content_agent",
    description=(
        "Recreates web page content optimized for SEO. "
        "Optimizes headings, paragraphs, meta tags, and image alt texts."
    ),
    instruction=prompt.SEO_CONTENT_RECREATOR_PROMPT,
    output_key="seo_content_recreator_output",
    tools=[
        optimize_title_tag,
        optimize_meta_description,
        optimize_headings,
        optimize_paragraph_content,
        generate_image_alt_texts
    ]
)

edit_content_agent = Agent(
    model=MODEL,
    name="edit_content_agent",
    description=(
        "Recreates web page content optimized for SEO. "
        "Optimizes headings, paragraphs, meta tags, and image alt texts."
    ),
    instruction=prompt.EDIT_CONTENT_ORCHESTRATOR_PROMPT,
    output_key="seo_content_recreator_output",
    sub_agents=[edit_text_content_agent, image_generator_agent]
)
