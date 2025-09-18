from typing import Dict, Any, List
from datetime import datetime
from bs4 import BeautifulSoup, Tag

from google.adk.tools.tool_context import ToolContext

from app.utils.web_crawler import crawl_webpage



async def extract_html_content(
        tool_context: ToolContext,
        url: str = ""
) -> Dict[str, Any]:
    """
    Extracts and catalogs HTML content elements from a web page.

    Args:
        tool_context: ADK tool context
        url: URL of the web page to analyze

    Returns:
        Complete HTML content extraction results
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

        soup = BeautifulSoup(crawl_data['html_content'], 'html.parser')

        headings = extract_heading_elements(soup)

        paragraphs = extract_paragraph_elements(soup)

        divisions = extract_div_elements(soup)

        summary = generate_extraction_summary(headings, paragraphs, divisions)

        detailed_report = generate_detailed_report(url, headings, paragraphs, divisions, summary)

        result = {
            "status": "success",
            "url": url,
            "extraction_timestamp": datetime.now().isoformat(),
            "headings": headings,
            "paragraphs": paragraphs,
            "divisions": divisions,
            "summary": summary,
            "detailed_report": detailed_report,
            "total_elements": sum([
                len(headings.get('h1', [])),
                len(headings.get('h2', [])),
                len(headings.get('h3', [])),
                len(headings.get('h4', [])),
                len(headings.get('h5', [])),
                len(headings.get('h6', [])),
                len(paragraphs),
                len(divisions)
            ])
        }

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during HTML content extraction: {str(e)}",
            "url": url
        }


async def extract_specific_tags(
        tool_context: ToolContext,
        url: str = "",
        tag_types: str = "h1,h2,h3,p"
) -> Dict[str, Any]:
    """
    Extracts content from specific HTML tag types only.

    Args:
        tool_context: ADK tool context
        url: URL of the web page to analyze
        tag_types: Comma-separated list of tag types to extract (e.g., "h1,h2,p,div")

    Returns:
        Filtered HTML content extraction results
    """
    if not url:
        return {
            "status": "error",
            "message": "URL parameter is required"
        }

    try:
        requested_tags = [tag.strip().lower() for tag in tag_types.split(",")]

        crawl_data = crawl_webpage(url)

        if 'error' in crawl_data:
            return {
                "status": "error",
                "message": f"Error crawling web page: {crawl_data['error']}",
                "url": url
            }

        soup = BeautifulSoup(crawl_data['html_content'], 'html.parser')

        extracted_content = {}

        for tag_type in requested_tags:
            if tag_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if 'headings' not in extracted_content:
                    extracted_content['headings'] = {}
                extracted_content['headings'][tag_type] = extract_specific_heading(soup, tag_type)
            elif tag_type == 'p':
                extracted_content['paragraphs'] = extract_paragraph_elements(soup)
            elif tag_type == 'div':
                extracted_content['divisions'] = extract_div_elements(soup)

        total_elements = 0
        for category, content in extracted_content.items():
            if isinstance(content, dict):
                total_elements += sum(len(items) for items in content.values())
            elif isinstance(content, list):
                total_elements += len(content)

        result = {
            "status": "success",
            "url": url,
            "requested_tags": requested_tags,
            "extraction_timestamp": datetime.now().isoformat(),
            "extracted_content": extracted_content,
            "total_elements": total_elements,
            "summary": f"Extracted {total_elements} elements from {len(requested_tags)} tag types"
        }

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during specific tag extraction: {str(e)}",
            "url": url
        }


def extract_heading_elements(soup: BeautifulSoup) -> Dict[str, List[Dict[str, Any]]]:
    """Extract all heading elements (H1-H6) with their content and attributes."""
    headings = {}

    for level in range(1, 7):
        tag_name = f'h{level}'
        heading_tags = soup.find_all(tag_name)

        headings[tag_name] = []

        for i, tag in enumerate(heading_tags, 1):
            heading_info = {
                "index": i,
                "content": tag.get_text().strip(),
                "attributes": dict(tag.attrs) if tag.attrs else {},
                "position": get_element_position(tag),
                "depth_level": get_nesting_depth(tag),
                "character_count": len(tag.get_text().strip()),
                "has_nested_elements": bool(tag.find_all()),
                "parent_tag": tag.parent.name if tag.parent else None
            }
            headings[tag_name].append(heading_info)

    return headings


def extract_paragraph_elements(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract all paragraph elements with their content and attributes."""
    paragraph_tags = soup.find_all('p')
    paragraphs = []

    for i, tag in enumerate(paragraph_tags, 1):
        paragraph_info = {
            "index": i,
            "content": tag.get_text().strip(),
            "attributes": dict(tag.attrs) if tag.attrs else {},
            "word_count": len(tag.get_text().strip().split()),
            "character_count": len(tag.get_text().strip()),
            "position": get_element_position(tag),
            "parent_tag": tag.parent.name if tag.parent else None,
            "has_links": bool(tag.find_all('a')),
            "has_formatting": bool(tag.find_all(['strong', 'em', 'b', 'i', 'span'])),
            "is_empty": len(tag.get_text().strip()) == 0
        }
        paragraphs.append(paragraph_info)

    return paragraphs


def extract_div_elements(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract all div elements with their content and structural information."""
    div_tags = soup.find_all('div')
    divisions = []

    for i, tag in enumerate(div_tags, 1):
        full_content = tag.get_text().strip()
        content_preview = full_content[:100] + "..." if len(full_content) > 100 else full_content

        # Get child element types
        child_elements = [child.name for child in tag.find_all() if child.name]
        unique_child_types = list(set(child_elements))

        division_info = {
            "index": i,
            "content_preview": content_preview,
            "full_content_length": len(full_content),
            "attributes": dict(tag.attrs) if tag.attrs else {},
            "child_elements": unique_child_types,
            "total_child_count": len(child_elements),
            "position": get_element_position(tag),
            "nesting_level": get_nesting_depth(tag),
            "parent_tag": tag.parent.name if tag.parent else None,
            "has_id": bool(tag.get('id')),
            "has_class": bool(tag.get('class')),
            "is_empty": len(full_content) == 0
        }
        divisions.append(division_info)

    return divisions


def extract_specific_heading(soup: BeautifulSoup, tag_name: str) -> List[Dict[str, Any]]:
    """Extract specific heading type (h1, h2, etc.) with detailed information."""
    heading_tags = soup.find_all(tag_name)
    headings = []

    for i, tag in enumerate(heading_tags, 1):
        heading_info = {
            "index": i,
            "content": tag.get_text().strip(),
            "attributes": dict(tag.attrs) if tag.attrs else {},
            "position": get_element_position(tag),
            "depth_level": get_nesting_depth(tag),
            "character_count": len(tag.get_text().strip()),
            "parent_tag": tag.parent.name if tag.parent else None
        }
        headings.append(heading_info)

    return headings


def get_element_position(tag: Tag) -> int:
    """Get the approximate line position of an element in the document."""

    all_elements = tag.find_parent().find_all() if tag.find_parent() else []
    try:
        return all_elements.index(tag) + 1
    except ValueError:
        return 0


def get_nesting_depth(tag: Tag) -> int:
    """Calculate the nesting depth of an element."""
    depth = 0
    current = tag.parent
    while current and current.name:
        depth += 1
        current = current.parent
    return depth


def generate_extraction_summary(
        headings: Dict[str, List[Dict[str, Any]]],
        paragraphs: List[Dict[str, Any]],
        divisions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate comprehensive summary of extracted content."""

    heading_counts = {tag: len(items) for tag, items in headings.items()}

    total_paragraph_words = sum(p.get('word_count', 0) for p in paragraphs)
    avg_paragraph_length = total_paragraph_words / len(paragraphs) if paragraphs else 0

    max_nesting_level = max((d.get('nesting_level', 0) for d in divisions), default=0)

    all_classes = []
    for p in paragraphs:
        classes = p.get('attributes', {}).get('class', [])
        if isinstance(classes, list):
            all_classes.extend(classes)

    for d in divisions:
        classes = d.get('attributes', {}).get('class', [])
        if isinstance(classes, list):
            all_classes.extend(classes)

    from collections import Counter
    common_classes = Counter(all_classes).most_common(5)

    summary = {
        "heading_counts": heading_counts,
        "total_headings": sum(heading_counts.values()),
        "total_paragraphs": len(paragraphs),
        "total_divisions": len(divisions),
        "average_paragraph_length": round(avg_paragraph_length, 1),
        "max_nesting_level": max_nesting_level,
        "most_common_classes": [{"class": cls, "count": count} for cls, count in common_classes],
        "content_density": "high" if total_paragraph_words > 1000 else "medium" if total_paragraph_words > 300 else "low",
        "structural_complexity": "high" if max_nesting_level > 5 else "medium" if max_nesting_level > 2 else "low"
    }

    return summary


def generate_detailed_report(
        url: str,
        headings: Dict[str, List[Dict[str, Any]]],
        paragraphs: List[Dict[str, Any]],
        divisions: List[Dict[str, Any]],
        summary: Dict[str, Any]
) -> str:
    """Generate a detailed text report of the extraction results."""
    report = []
    report.append("HTML Content Extraction Report")
    report.append("=" * 40)
    report.append(f"URL: {url}")
    report.append(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(
        f"Total Elements Extracted: {summary['total_headings'] + summary['total_paragraphs'] + summary['total_divisions']}")
    report.append("")

    report.append("📋 HEADING ELEMENTS (H1-H6):")
    for tag_name, items in headings.items():
        if items:
            report.append(f"{tag_name.upper()} Elements ({len(items)} found):")
            for item in items[:3]:
                report.append(
                    f"  {item['index']}. Content: \"{item['content'][:50]}{'...' if len(item['content']) > 50 else ''}\"")
                if item['attributes']:
                    report.append(f"     Attributes: {item['attributes']}")
                report.append(f"     Position: {item['position']}, Depth: {item['depth_level']}")
            if len(items) > 3:
                report.append(f"     ... and {len(items) - 3} more")
            report.append("")

    report.append("📝 PARAGRAPH ELEMENTS (P):")
    for i, para in enumerate(paragraphs[:5], 1):
        content_preview = para['content'][:80] + "..." if len(para['content']) > 80 else para['content']
        report.append(f"Paragraph {i}:")
        report.append(f"  Content: \"{content_preview}\"")
        report.append(f"  Word Count: {para['word_count']} words")
        if para['attributes']:
            report.append(f"  Attributes: {para['attributes']}")
        report.append(f"  Position: {para['position']}, Parent: {para['parent_tag']}")
        report.append("")

    if len(paragraphs) > 5:
        report.append(f"... and {len(paragraphs) - 5} more paragraphs")
        report.append("")

    report.append("📦 DIVISION ELEMENTS (DIV):")
    for i, div in enumerate(divisions[:5], 1):
        report.append(f"Division {i}:")
        report.append(f"  Content Preview: \"{div['content_preview']}\"")
        report.append(f"  Full Content Length: {div['full_content_length']} characters")
        if div['attributes']:
            report.append(f"  Attributes: {div['attributes']}")
        report.append(f"  Child Elements: {div['child_elements']}")
        report.append(f"  Position: {div['position']}, Nesting Level: {div['nesting_level']}")
        report.append("")

    if len(divisions) > 5:
        report.append(f"... and {len(divisions) - 5} more divisions")
        report.append("")

    report.append("📊 EXTRACTION SUMMARY:")
    for tag, count in summary['heading_counts'].items():
        report.append(f"- Total {tag.upper()} Tags: {count}")
    report.append(f"- Total P Tags: {summary['total_paragraphs']}")
    report.append(f"- Total DIV Tags: {summary['total_divisions']}")
    report.append(f"- Average Paragraph Length: {summary['average_paragraph_length']} words")
    report.append(f"- Deepest Nesting Level: {summary['max_nesting_level']}")
    report.append(f"- Content Density: {summary['content_density']}")
    report.append(f"- Structural Complexity: {summary['structural_complexity']}")
    report.append("")

    report.append("🔍 CONTENT ANALYSIS:")
    if summary['most_common_classes']:
        report.append("- Most Common Classes:")
        for cls_info in summary['most_common_classes']:
            report.append(f"  • {cls_info['class']}: {cls_info['count']} occurrences")
    else:
        report.append("- No common CSS classes found")

    return "\n".join(report)
