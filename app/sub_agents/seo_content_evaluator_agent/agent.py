import os
from typing import Dict, Any
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools.tool_context import ToolContext

from . import prompt
from app.tools.html_parser import extract_html_content, extract_specific_tags
from app.tools.seo_analyze import analyze_webpage_seo, extract_page_keywords
from app.tools.memory import memorize
from ...tools.output_parser import modify_output_after_agent, simple_after_model_modifier

MODEL = "gemini-2.5-pro"
load_dotenv()

html_content_extractor_agent = Agent(
    model=MODEL,
    name="html_content_extractor_agent",
    description=(
        "Extracts and catalogs HTML content elements from web pages. "
        "Specializes in extracting H1-H6 headings, paragraphs, and div elements with detailed structural analysis."
    ),
    instruction=prompt.HTML_CONTENT_EXTRACTOR_PROMPT,
    output_key="html_content_extractor_output",
    tools=[extract_html_content, extract_specific_tags, memorize]
)

content_seo_ruler_agent = Agent(
    model=MODEL,
    name="content_seo_ruler_agent",
    description=(
        "Crawls web pages and checks their SEO compliance. "
        "Extracts most frequently used keywords and performs detailed SEO analysis."
    ),
    instruction=prompt.CONTENT_SEO_RULER_PROMPT,
    output_key="content_seo_ruler_output",
    tools=[analyze_webpage_seo, extract_page_keywords, memorize],
    after_model_callback=simple_after_model_modifier
)

seo_content_evaluator_agent = Agent(
    model=MODEL,
    name="seo_content_evaluator_agent",
    description=(
        "Crawls web pages and checks their SEO compliance. "
        "Extracts most frequently used keywords and performs detailed SEO analysis."
    ),
    instruction=prompt.CONTENT_SEO_EVALUATOR_PROMPT,
    output_key="content_seo_ruler_output",
    sub_agents=[html_content_extractor_agent,content_seo_ruler_agent],
    tools=[memorize]
)