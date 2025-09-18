from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools.tool_context import ToolContext

async def optimize_title_tag(
        tool_context: ToolContext,
        current_title: str = "",
        target_keywords: str = "",
        brand_name: str = ""
) -> Dict[str, Any]:
    """
    Optimizes title tag according to SEO rules.

    Args:
        tool_context: ADK tool context
        current_title: Current title tag
        target_keywords: Target keywords (comma separated)
        brand_name: Brand name (optional)

    Returns:
        Optimized title suggestions
    """
    if not current_title and not target_keywords:
        return {
            "status": "error",
            "message": "Current title or target keywords are required"
        }

    try:
        keywords_list = [kw.strip() for kw in target_keywords.split(",")] if target_keywords else []
        main_keyword = keywords_list[0] if keywords_list else ""

        # Create title optimization suggestions
        optimized_titles = []

        if main_keyword:
            # Titles starting with main keyword
            if brand_name:
                optimized_titles.extend([
                    f"{main_keyword} - {brand_name}",
                    f"{main_keyword} | {brand_name}",
                    f"Best {main_keyword} - {brand_name}"
                ])
            else:
                optimized_titles.extend([
                    f"{main_keyword} - Comprehensive Guide",
                    f"Best {main_keyword} Solutions",
                    f"Everything You Need to Know About {main_keyword}"
                ])

        # Optimize current title
        if current_title:
            # Length check
            current_length = len(current_title)
            if current_length > 60:
                # Shorten
                optimized_titles.append(current_title[:57] + "...")
            elif current_length < 30:
                # Expand
                if main_keyword and main_keyword.lower() not in current_title.lower():
                    optimized_titles.append(f"{main_keyword} - {current_title}")

        # Select best 3 suggestions
        final_suggestions = optimized_titles[:3]

        return {
            "status": "success",
            "original_title": current_title,
            "original_length": len(current_title),
            "optimized_titles": [
                {
                    "title": title,
                    "length": len(title),
                    "seo_score": _calculate_title_seo_score(title, keywords_list)
                }
                for title in final_suggestions
            ],
            "recommendations": [
                "Title should be 30-60 characters long",
                "Primary keyword should be at the beginning",
                "Brand name should be at the end",
                "Should be clickable and compelling"
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during title optimization: {str(e)}"
        }


async def optimize_meta_description(
        tool_context: ToolContext,
        current_description: str = "",
        target_keywords: str = "",
        page_content_summary: str = ""
) -> Dict[str, Any]:
    """
    Optimizes meta description according to SEO rules.

    Args:
        tool_context: ADK tool context
        current_description: Current meta description
        target_keywords: Target keywords
        page_content_summary: Page content summary

    Returns:
        Optimized meta description suggestions
    """
    try:
        keywords_list = [kw.strip() for kw in target_keywords.split(",")] if target_keywords else []
        main_keyword = keywords_list[0] if keywords_list else ""

        optimized_descriptions = []

        # Keyword-based descriptions
        if main_keyword:
            optimized_descriptions.extend([
                f"Comprehensive information about {main_keyword}. Discover the best solutions with expert guidance. Check it out now!",
                f"Learn the best {main_keyword} solutions. Achieve success with detailed guides and practical tips.",
                f"Everything you're looking for about {main_keyword} is here. Click for expert advice and current information."
            ])

        # Content-based description
        if page_content_summary:
            summary_words = page_content_summary.split()[:20]  # First 20 words
            content_based = " ".join(summary_words)
            if main_keyword and main_keyword.lower() not in content_based.lower():
                content_based = f"{main_keyword} - {content_based}"

            # Adjust to 160 character limit
            if len(content_based) > 157:
                content_based = content_based[:154] + "..."

            optimized_descriptions.append(content_based)

        # Optimize current description
        if current_description:
            current_length = len(current_description)
            if current_length > 160:
                optimized_descriptions.append(current_description[:157] + "...")
            elif current_length < 120 and main_keyword:
                if main_keyword.lower() not in current_description.lower():
                    extended = f"{main_keyword} - {current_description}"
                    if len(extended) <= 160:
                        optimized_descriptions.append(extended)

        # Select best 3 suggestions
        final_suggestions = optimized_descriptions[:3]

        return {
            "status": "success",
            "original_description": current_description,
            "original_length": len(current_description),
            "optimized_descriptions": [
                {
                    "description": desc,
                    "length": len(desc),
                    "seo_score": _calculate_meta_seo_score(desc, keywords_list)
                }
                for desc in final_suggestions
            ],
            "recommendations": [
                "Meta description should be 120-160 characters long",
                "Should include primary keyword",
                "Should include call-to-action (CTA)",
                "Should summarize page content"
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during meta description optimization: {str(e)}"
        }


async def optimize_headings(
        tool_context: ToolContext,
        headings_data: str = "",
        target_keywords: str = "",
        content_context: str = ""
) -> Dict[str, Any]:
    """
    Optimizes heading tags (H1-H4) according to SEO rules.

    Args:
        tool_context: ADK tool context
        headings_data: Current headings (JSON format)
        target_keywords: Target keywords
        content_context: Content context

    Returns:
        Optimized heading suggestions
    """
    try:
        import json

        # Parse heading data
        try:
            headings = json.loads(headings_data) if headings_data else {}
        except json.JSONDecodeError:
            # Accept as simple format
            headings = {"h1": [headings_data]} if headings_data else {}

        keywords_list = [kw.strip() for kw in target_keywords.split(",")] if target_keywords else []
        main_keyword = keywords_list[0] if keywords_list else ""

        optimized_headings = {
            "h1": [],
            "h2": [],
            "h3": [],
            "h4": []
        }

        # H1 optimization
        current_h1 = headings.get("h1", [])
        if current_h1:
            for h1 in current_h1:
                if main_keyword and main_keyword.lower() not in h1.lower():
                    optimized_headings["h1"].append(f"{main_keyword}: {h1}")
                else:
                    optimized_headings["h1"].append(h1)
        elif main_keyword:
            optimized_headings["h1"].extend([
                f"{main_keyword} Guide",
                f"Best {main_keyword} Solutions",
                f"Everything You Need to Know About {main_keyword}"
            ])

        # H2 optimization
        current_h2 = headings.get("h2", [])
        if keywords_list:
            for i, keyword in enumerate(keywords_list[1:4], 1):  # Secondary keywords
                optimized_headings["h2"].append(f"What is {keyword}?")
                optimized_headings["h2"].append(f"How to Use {keyword}?")

        if current_h2:
            for h2 in current_h2:
                optimized_headings["h2"].append(h2)

        # General suggestions for H3 and H4
        if main_keyword:
            optimized_headings["h3"].extend([
                f"{main_keyword} Benefits",
                f"{main_keyword} Features",
                "Frequently Asked Questions"
            ])

            optimized_headings["h4"].extend([
                "Practical Tips",
                "Expert Recommendations",
                "Conclusion and Recommendations"
            ])

        return {
            "status": "success",
            "original_headings": headings,
            "optimized_headings": optimized_headings,
            "seo_improvements": [
                "H1 tag should contain primary keyword",
                "H2 tags should use secondary keywords",
                "Heading hierarchy should be logical",
                "Each heading should be unique and descriptive"
            ],
            "hierarchy_check": _check_heading_hierarchy(optimized_headings)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during heading optimization: {str(e)}"
        }


async def optimize_paragraph_content(
        tool_context: ToolContext,
        paragraph_text: str = "",
        target_keywords: str = "",
        min_words: int = 20
) -> Dict[str, Any]:
    """
    Optimizes paragraph content according to SEO rules.

    Args:
        tool_context: ADK tool context
        paragraph_text: Current paragraph text
        target_keywords: Target keywords
        min_words: Minimum word count

    Returns:
        Optimized paragraph suggestions
    """
    try:
        if not paragraph_text:
            return {
                "status": "error",
                "message": "Paragraph text is required"
            }

        keywords_list = [kw.strip() for kw in target_keywords.split(",")] if target_keywords else []
        main_keyword = keywords_list[0] if keywords_list else ""

        # Current paragraph analysis
        word_count = len(paragraph_text.split())
        current_density = _calculate_keyword_density(paragraph_text, main_keyword) if main_keyword else 0

        optimized_paragraphs = []

        # Expand short paragraphs
        if word_count < min_words:
            expanded_text = paragraph_text

            # Keyword-based expansion
            if main_keyword:
                if main_keyword.lower() not in expanded_text.lower():
                    expanded_text = f"This content about {main_keyword} provides valuable insights. {expanded_text}"

                # Additional informative sentences
                additional_sentences = [
                    f"This {main_keyword} solution offers multiple benefits for users.",
                    f"Experts recommend this approach for {main_keyword} optimization.",
                    f"For more information about {main_keyword}, continue reading below."
                ]

                expanded_text += " " + additional_sentences[0]
            else:
                # Generic expansion without keywords
                expanded_text += " This information provides valuable insights and practical guidance for better understanding."

            optimized_paragraphs.append(expanded_text)

        # Optimize keyword density
        if current_density > 3.0 and main_keyword:
            # Reduce density by replacing one occurrence
            reduced_text = paragraph_text.replace(main_keyword, "this topic", 1)
            optimized_paragraphs.append(reduced_text)
        elif current_density < 1.0 and main_keyword and word_count >= min_words:
            # Increase density by adding keyword naturally
            words = paragraph_text.split()
            middle_index = len(words) // 2
            words.insert(middle_index, main_keyword)
            increased_text = " ".join(words)
            optimized_paragraphs.append(increased_text)

        # Improve readability
        readable_text = _improve_readability(paragraph_text, keywords_list)
        if readable_text != paragraph_text:
            optimized_paragraphs.append(readable_text)

        # Ensure at least one suggestion
        if not optimized_paragraphs:
            # Provide a basic optimization
            if main_keyword and main_keyword.lower() not in paragraph_text.lower():
                optimized_text = f"When considering {main_keyword}, it's important to note that {paragraph_text}"
                optimized_paragraphs.append(optimized_text)
            else:
                optimized_paragraphs.append(paragraph_text)

        return {
            "status": "success",
            "original_paragraph": paragraph_text,
            "original_word_count": word_count,
            "original_keyword_density": current_density,
            "optimized_paragraphs": [
                {
                    "text": para,
                    "word_count": len(para.split()),
                    "keyword_density": _calculate_keyword_density(para, main_keyword) if main_keyword else 0,
                    "readability_score": _calculate_readability_score(para)
                }
                for para in optimized_paragraphs
            ],
            "seo_improvements": [
                f"Paragraphs should contain at least {min_words} words",
                "Keyword density should be between 1-3%",
                "Use short and clear sentences",
                "Add transition words for better flow"
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during paragraph optimization: {str(e)}"
        }


async def generate_image_alt_texts(
        tool_context: ToolContext,
        image_descriptions: str = "",
        target_keywords: str = "",
        page_context: str = ""
) -> Dict[str, Any]:
    """
    Generates SEO-friendly alt texts for images.

    Args:
        tool_context: ADK tool context
        image_descriptions: Image descriptions (comma separated)
        target_keywords: Target keywords
        page_context: Page context

    Returns:
        SEO-friendly alt text suggestions
    """
    try:
        descriptions = [desc.strip() for desc in image_descriptions.split(",")] if image_descriptions else []
        keywords_list = [kw.strip() for kw in target_keywords.split(",")] if target_keywords else []
        main_keyword = keywords_list[0] if keywords_list else ""

        alt_texts = []

        for i, desc in enumerate(descriptions):
            if not desc:
                continue

            if main_keyword and main_keyword.lower() not in desc.lower():
                alt_text = f"{main_keyword} - {desc}"
            else:
                alt_text = desc

            if len(alt_text) > 125:
                alt_text = alt_text[:122] + "..."

            alt_texts.append({
                "image_index": i + 1,
                "original_description": desc,
                "optimized_alt_text": alt_text,
                "length": len(alt_text),
                "contains_keyword": main_keyword.lower() in alt_text.lower() if main_keyword else False
            })

        if not descriptions and main_keyword:
            general_alts = [
                f"{main_keyword} example",
                f"{main_keyword} image",
                f"Image related to {main_keyword}"
            ]

            for i, alt in enumerate(general_alts):
                alt_texts.append({
                    "image_index": i + 1,
                    "original_description": "",
                    "optimized_alt_text": alt,
                    "length": len(alt),
                    "contains_keyword": True
                })

        return {
            "status": "success",
            "total_images": len(alt_texts),
            "alt_texts": alt_texts,
            "seo_guidelines": [
                "Alt texts should be shorter than 125 characters",
                "Should include keywords but naturally",
                "Should be descriptive and specific",
                "Should be accessible for visually impaired users"
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during alt text generation: {str(e)}"
        }


def _calculate_title_seo_score(title: str, keywords: List[str]) -> int:
    score = 0
    title_lower = title.lower()

    if 30 <= len(title) <= 60:
        score += 30

    if keywords and keywords[0].lower() in title_lower:
        score += 40
        if title_lower.startswith(keywords[0].lower()):
            score += 20

    for keyword in keywords[1:3]:
        if keyword.lower() in title_lower:
            score += 10

    return min(score, 100)


def _calculate_meta_seo_score(description: str, keywords: List[str]) -> int:
    score = 0
    desc_lower = description.lower()

    if 120 <= len(description) <= 160:
        score += 40

    if keywords and keywords[0].lower() in desc_lower:
        score += 30

    cta_words = ['click', 'explore', 'discover', 'learn', 'start']
    if any(cta in desc_lower for cta in cta_words):
        score += 20

    for keyword in keywords[1:3]:
        if keyword.lower() in desc_lower:
            score += 10

    return min(score, 100)


def _calculate_keyword_density(text: str, keyword: str) -> float:
    """Calculates keyword density."""
    if not keyword or not text:
        return 0.0

    text_lower = text.lower()
    keyword_lower = keyword.lower()

    words = text_lower.split()
    keyword_count = text_lower.count(keyword_lower)

    if not words:
        return 0.0

    density = (keyword_count / len(words)) * 100
    return round(density, 2)


def _improve_readability(text: str, keywords: List[str]) -> str:
    """Improves text readability."""
    sentences = text.split('.')
    improved_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        words = sentence.split()
        if len(words) > 20:
            mid = len(words) // 2
            part1 = ' '.join(words[:mid])
            part2 = ' '.join(words[mid:])
            improved_sentences.extend([part1, part2])
        else:
            improved_sentences.append(sentence)

    return '. '.join(improved_sentences) + '.'


def _calculate_readability_score(text: str) -> int:
    """Calculates simple readability score."""
    sentences = text.split('.')
    words = text.split()

    if not sentences or not words:
        return 0

    avg_words_per_sentence = len(words) / len(sentences)

    if avg_words_per_sentence <= 15:
        return 90
    elif avg_words_per_sentence <= 20:
        return 70
    elif avg_words_per_sentence <= 25:
        return 50
    else:
        return 30


def _check_heading_hierarchy(headings: Dict[str, List[str]]) -> Dict[str, Any]:
    """Checks heading hierarchy."""
    h1_count = len(headings.get("h1", []))
    h2_count = len(headings.get("h2", []))
    h3_count = len(headings.get("h3", []))
    h4_count = len(headings.get("h4", []))

    issues = []

    if h1_count == 0:
        issues.append("H1 tag missing")
    elif h1_count > 1:
        issues.append("Multiple H1 tag")

    if h2_count == 0 and (h3_count > 0 or h4_count > 0):
        issues.append("H3/H4 used without H2")

    if h3_count == 0 and h4_count > 0:
        issues.append("H4 used without H3")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "counts": {
            "h1": h1_count,
            "h2": h2_count,
            "h3": h3_count,
            "h4": h4_count
        }
    }
