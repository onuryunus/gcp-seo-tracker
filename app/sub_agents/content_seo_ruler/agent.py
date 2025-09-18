# Copyright 2025 Google LLC
# Apache 2.0

"""ContentSEORuler agent: Crawls web pages and checks SEO rules compliance"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools.tool_context import ToolContext

from . import prompt
from ...utils.web_crawler import crawl_webpage
from ...utils.seo_analyzer import SEOAnalyzer

MODEL = "gemini-2.5-pro"
load_dotenv()


async def analyze_webpage_seo(
    tool_context: ToolContext,
    url: str = ""
) -> Dict[str, Any]:
    """
    Crawls a web page and checks its SEO compliance.
    
    Args:
        tool_context: ADK tool context
        url: URL of the web page to analyze
        
    Returns:
        SEO analysis results
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
        
        seo_analyzer = SEOAnalyzer()
        seo_analysis = seo_analyzer.analyze_seo(crawl_data)
        
        detailed_report = seo_analyzer.generate_seo_report_with_keywords(seo_analysis, crawl_data.get('keywords', []))
        
        result = {
            "status": "success",
            "url": url,
            "seo_score": seo_analysis.get('seo_score', 0),
            "total_checks": seo_analysis.get('total_checks', 0),
            "passed_checks": seo_analysis.get('passed_checks', 0),
            "issues": seo_analysis.get('issues', []),
            "recommendations": seo_analysis.get('recommendations', []),
            "keywords": crawl_data.get('keywords', [])[:20],
            "detailed_report": detailed_report,
            "page_info": {
                "title": crawl_data.get('title'),
                "meta_description": crawl_data.get('meta_description'),
                "word_count": crawl_data.get('word_count', 0),
                "headings_count": {
                    "h1": len(crawl_data.get('headings', {}).get('h1', [])),
                    "h2": len(crawl_data.get('headings', {}).get('h2', [])),
                    "h3": len(crawl_data.get('headings', {}).get('h3', [])),
                    "h4": len(crawl_data.get('headings', {}).get('h4', []))
                },
                "images_total": len(crawl_data.get('images', [])),
                "images_with_alt": sum(1 for img in crawl_data.get('images', []) if img.get('alt', '').strip())
            }
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during SEO analysis: {str(e)}",
            "url": url
        }


async def extract_page_keywords(
    tool_context: ToolContext,
    url: str = "",
    keyword_count: int = 20
) -> Dict[str, Any]:
    """
    Extracts keywords from a web page.
    
    Args:
        tool_context: ADK tool context
        url: URL of the web page to analyze
        keyword_count: Number of keywords to extract
        
    Returns:
        List of keywords
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
        
        keywords = crawl_data.get('keywords', [])[:keyword_count]
        
        return {
            "status": "success",
            "url": url,
            "keywords": keywords,
            "total_words": crawl_data.get('word_count', 0),
            "page_title": crawl_data.get('title', ''),
            "keyword_summary": f"{len(keywords)} keywords extracted"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during keyword extraction: {str(e)}",
            "url": url
        }


content_seo_ruler_agent = Agent(
    model=MODEL,
    name="content_seo_ruler_agent",
    description=(
        "Crawls web pages and checks their SEO compliance. "
        "Extracts most frequently used keywords and performs detailed SEO analysis."
    ),
    instruction=prompt.CONTENT_SEO_RULER_PROMPT,
    output_key="content_seo_ruler_output",
    tools=[analyze_webpage_seo, extract_page_keywords]
)
