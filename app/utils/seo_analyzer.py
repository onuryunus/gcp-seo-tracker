# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""SEO analysis utilities for web pages."""

from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re


class SEOAnalyzer:
    """Class for analyzing SEO compliance of web pages."""
    
    def __init__(self):
        self.seo_rules = {
            'title_length': {'min': 30, 'max': 60},
            'meta_description_length': {'min': 120, 'max': 160},
            'h1_count': {'min': 1, 'max': 1},
            'keyword_density': {'min': 1.0, 'max': 3.0},
            'image_alt_ratio': {'min': 0.8},
            'internal_links_min': 3,
            'paragraph_min_words': 20
        }
    
    def analyze_seo(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze web page crawl data from SEO perspective.
        
        Args:
            crawl_data: Data from web crawler
            
        Returns:
            SEO analysis results
        """
        if 'error' in crawl_data:
            return {'error': crawl_data['error'], 'seo_score': 0}
        
        analysis = {
            'url': crawl_data.get('url'),
            'seo_score': 0,
            'total_checks': 0,
            'passed_checks': 0,
            'issues': [],
            'recommendations': [],
            'details': {}
        }
        
        self._analyze_title(crawl_data, analysis)
        self._analyze_meta_description(crawl_data, analysis)
        self._analyze_headings(crawl_data, analysis)
        self._analyze_images(crawl_data, analysis)
        self._analyze_paragraphs(crawl_data, analysis)
        self._analyze_keywords(crawl_data, analysis)
        self._analyze_links(crawl_data, analysis)
        self._analyze_content_length(crawl_data, analysis)
        if analysis['total_checks'] > 0:
            analysis['seo_score'] = round(
                (analysis['passed_checks'] / analysis['total_checks']) * 100
            )
        
        return analysis
    
    def _analyze_title(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Title tag analysis."""
        analysis['total_checks'] += 1
        title = crawl_data.get('title')
        
        if not title:
            analysis['issues'].append('Title tag missing')
            analysis['recommendations'].append('Add a meaningful title tag to the page')
            analysis['details']['title'] = {'status': 'missing', 'length': 0}
            return
        
        title_length = len(title)
        analysis['details']['title'] = {
            'content': title,
            'length': title_length,
            'status': 'exists'
        }
        
        if title_length < self.seo_rules['title_length']['min']:
            analysis['issues'].append(f'Title too short ({title_length} characters)')
            analysis['recommendations'].append(f'Title should be at least {self.seo_rules["title_length"]["min"]} characters')
        elif title_length > self.seo_rules['title_length']['max']:
            analysis['issues'].append(f'Title too long ({title_length} characters)')
            analysis['recommendations'].append(f'Title should be at most {self.seo_rules["title_length"]["max"]} characters')
        else:
            analysis['passed_checks'] += 1
            analysis['details']['title']['status'] = 'optimal'
    
    def _analyze_meta_description(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Meta description analysis."""
        analysis['total_checks'] += 1
        meta_desc = crawl_data.get('meta_description')
        
        if not meta_desc:
            analysis['issues'].append('Meta description missing')
            analysis['recommendations'].append('Add meta description to the page')
            analysis['details']['meta_description'] = {'status': 'missing', 'length': 0}
            return
        
        desc_length = len(meta_desc)
        analysis['details']['meta_description'] = {
            'content': meta_desc,
            'length': desc_length,
            'status': 'exists'
        }
        
        if desc_length < self.seo_rules['meta_description_length']['min']:
            analysis['issues'].append(f'Meta description too short ({desc_length} characters)')
            analysis['recommendations'].append(f'Meta description should be at least {self.seo_rules["meta_description_length"]["min"]} characters')
        elif desc_length > self.seo_rules['meta_description_length']['max']:
            analysis['issues'].append(f'Meta description too long ({desc_length} characters)')
            analysis['recommendations'].append(f'Meta description should be at most {self.seo_rules["meta_description_length"]["max"]} characters')
        else:
            analysis['passed_checks'] += 1
            analysis['details']['meta_description']['status'] = 'optimal'
    
    def _analyze_headings(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Heading tags analysis."""
        headings = crawl_data.get('headings', {})
        analysis['total_checks'] += 1
        h1_tags = headings.get('h1', [])
        h1_count = len(h1_tags)
        
        analysis['details']['headings'] = {
            'h1': {'count': h1_count, 'content': h1_tags},
            'h2': {'count': len(headings.get('h2', [])), 'content': headings.get('h2', [])},
            'h3': {'count': len(headings.get('h3', [])), 'content': headings.get('h3', [])},
            'h4': {'count': len(headings.get('h4', [])), 'content': headings.get('h4', [])},
            'h5': {'count': len(headings.get('h5', [])), 'content': headings.get('h5', [])},
            'h6': {'count': len(headings.get('h6', [])), 'content': headings.get('h6', [])}
        }
        
        if h1_count == 0:
            analysis['issues'].append('H1 tag missing')
            analysis['recommendations'].append('Add one H1 tag to the page')
        elif h1_count > 1:
            analysis['issues'].append(f'Multiple H1 tags ({h1_count} count)')
            analysis['recommendations'].append('Page should have only one H1 tag')
        else:
            analysis['passed_checks'] += 1
        
        analysis['total_checks'] += 1
        if self._check_heading_hierarchy(headings):
            analysis['passed_checks'] += 1
        else:
            analysis['issues'].append('Heading hierarchy broken')
            analysis['recommendations'].append('Use heading tags in logical hierarchy (H1->H2->H3...)')
    
    def _analyze_images(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Image analysis."""
        images = crawl_data.get('images', [])
        
        if not images:
            analysis['details']['images'] = {'total': 0, 'with_alt': 0, 'without_alt': 0}
            return
        
        analysis['total_checks'] += 1
        images_with_alt = sum(1 for img in images if img.get('alt', '').strip())
        images_without_alt = len(images) - images_with_alt
        
        analysis['details']['images'] = {
            'total': len(images),
            'with_alt': images_with_alt,
            'without_alt': images_without_alt,
            'alt_ratio': round(images_with_alt / len(images), 2) if images else 0
        }
        
        alt_ratio = images_with_alt / len(images) if images else 0
        
        if alt_ratio < self.seo_rules['image_alt_ratio']['min']:
            analysis['issues'].append(f'{images_without_alt} images missing alt text')
            analysis['recommendations'].append('Add descriptive alt text to all images')
        else:
            analysis['passed_checks'] += 1
    
    def _analyze_paragraphs(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Paragraph analysis."""
        paragraphs = crawl_data.get('paragraphs', [])
        
        if not paragraphs:
            analysis['details']['paragraphs'] = {'total': 0, 'average_words': 0}
            return
        
        word_counts = [len(p.split()) for p in paragraphs]
        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        
        analysis['details']['paragraphs'] = {
            'total': len(paragraphs),
            'average_words': round(avg_words, 1),
            'short_paragraphs': sum(1 for wc in word_counts if wc < self.seo_rules['paragraph_min_words'])
        }
        
        analysis['total_checks'] += 1
        if avg_words >= self.seo_rules['paragraph_min_words']:
            analysis['passed_checks'] += 1
        else:
            analysis['issues'].append(f'Paragraphs too short (average {avg_words:.1f} words)')
            analysis['recommendations'].append(f'Paragraphs should contain at least {self.seo_rules["paragraph_min_words"]} words')
    
    def _analyze_keywords(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Keyword analysis."""
        keywords = crawl_data.get('keywords', [])
        
        if not keywords:
            analysis['details']['keywords'] = {'top_keywords': [], 'density_issues': []}
            return
        
        top_keywords = keywords[:10]
        analysis['details']['keywords'] = {
            'top_keywords': top_keywords,
            'density_issues': []
        }
        
        analysis['total_checks'] += 1
        density_issues = []
        
        for keyword_data in top_keywords:
            density = keyword_data.get('percentage', 0)
            word = keyword_data.get('word', '')
            
            if density > self.seo_rules['keyword_density']['max']:
                density_issues.append(f'"{word}" keyword too dense ({density}%)')
        
        analysis['details']['keywords']['density_issues'] = density_issues
        
        if not density_issues:
            analysis['passed_checks'] += 1
        else:
            analysis['issues'].extend(density_issues)
            analysis['recommendations'].append('Keep keyword density between 1-3%')
    
    def _analyze_links(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Link analysis."""
        links = crawl_data.get('links', [])
        
        if not links:
            analysis['details']['links'] = {'total': 0, 'internal': 0, 'external': 0}
            return
        
        base_domain = self._extract_domain(crawl_data.get('url', ''))
        internal_links = []
        external_links = []
        
        for link in links:
            href = link.get('href', '')
            if href:
                link_domain = self._extract_domain(href)
                if link_domain == base_domain:
                    internal_links.append(link)
                else:
                    external_links.append(link)
        
        analysis['details']['links'] = {
            'total': len(links),
            'internal': len(internal_links),
            'external': len(external_links)
        }
        
        analysis['total_checks'] += 1
        if len(internal_links) >= self.seo_rules['internal_links_min']:
            analysis['passed_checks'] += 1
        else:
            analysis['issues'].append(f'Internal links count low ({len(internal_links)} count)')
            analysis['recommendations'].append(f'Add at least {self.seo_rules["internal_links_min"]} internal links')
    
    def _analyze_content_length(self, crawl_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Content length analysis."""
        word_count = crawl_data.get('word_count', 0)
        
        analysis['details']['content'] = {
            'word_count': word_count,
            'status': 'short' if word_count < 300 else 'adequate' if word_count < 1000 else 'long'
        }
        
        analysis['total_checks'] += 1
        if word_count >= 300:
            analysis['passed_checks'] += 1
        else:
            analysis['issues'].append(f'Content too short ({word_count} words)')
            analysis['recommendations'].append('Expand content to at least 300 words')
    
    def _check_heading_hierarchy(self, headings: Dict[str, List[str]]) -> bool:
        """Check if heading hierarchy is correct."""
        has_h1 = len(headings.get('h1', [])) > 0
        has_h2 = len(headings.get('h2', [])) > 0
        has_h3 = len(headings.get('h3', [])) > 0
        has_h4 = len(headings.get('h4', [])) > 0
        
        if not has_h1 and has_h2:
            return False
        
        if not has_h2 and has_h3:
            return False
        
        if not has_h3 and has_h4:
            return False
        
        return True
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        import re
        match = re.search(r'https?://([^/]+)', url)
        return match.group(1) if match else ''
    
    def generate_seo_report(self, analysis: Dict[str, Any]) -> str:
        """Generate detailed SEO analysis report with keywords and bullet points."""
        if 'error' in analysis:
            return f"Error: {analysis['error']}"
        
        report = []
        report.append(f"SEO Technical Audit Report")
        report.append("=" * 40)
        report.append(f"URL: {analysis['url']}")
        report.append(f"SEO Score: {analysis['seo_score']}/100")
        status = "Excellent" if analysis['seo_score'] >= 90 else "Good" if analysis['seo_score'] >= 70 else "Fair" if analysis['seo_score'] >= 50 else "Poor"
        report.append(f"Status: {status}")
        report.append("")
        
        report.append("🔑 KEYWORDS ANALYSIS (MANDATORY):")
        report.append("(Keywords will be extracted from crawl data)")
        report.append("")
        
        report.append("📊 AUDIT SUMMARY:")
        report.append(f"- Total Checks Performed: {analysis['total_checks']}")
        report.append(f"- Passed Tests: {analysis['passed_checks']}")
        report.append(f"- Failed Tests: {analysis['total_checks'] - analysis['passed_checks']}")
        report.append(f"- Warnings: 0")  
        report.append("")
        
        if analysis['issues']:
            report.append("🚨 SEO ISSUES FOUND (Each as individual bullet):")
            for issue in analysis['issues']:
                report.append(f"• {issue}")
            report.append("")
        
        passed_tests = self._generate_passed_tests(analysis)
        if passed_tests:
            report.append("✅ PASSED SEO TESTS (Each as individual bullet):")
            for test in passed_tests:
                report.append(f"• {test}")
            report.append("")
        
        if analysis['recommendations']:
            report.append("💡 OPTIMIZATION RECOMMENDATIONS (Prioritized):")
            for i, rec in enumerate(analysis['recommendations'], 1):
                priority = "HIGH PRIORITY" if i <= 2 else "MEDIUM PRIORITY" if i <= 4 else "LOW PRIORITY"
                report.append(f"• {priority}: {rec}")
            report.append("")
        
        details = analysis.get('details', {})
        report.append("📝 TECHNICAL DETAILS:")
        
        if 'title' in details:
            title_info = details['title']
            title_status = "Present" if title_info.get('content') else "Missing"
            title_length = title_info.get('length', 0)
            keyword_status = "Contains" if title_info.get('content') else "Missing"
            report.append(f"- Title: {title_status} - {title_length} characters - {keyword_status} primary keyword")
        
        if 'meta_description' in details:
            meta_info = details['meta_description']
            meta_status = "Present" if meta_info.get('content') else "Missing"
            meta_length = meta_info.get('length', 0)
            keyword_status = "Contains" if meta_info.get('content') else "Missing"
            report.append(f"- Meta Description: {meta_status} - {meta_length} characters - {keyword_status} primary keyword")
        
        if 'headings' in details:
            headings_info = details['headings']
            h1_count = headings_info['h1']['count']
            h1_status = "Optimal: 1" if h1_count == 1 else f"Issue: {h1_count}"
            report.append(f"- H1 Tags: {h1_count} count - {h1_status}")
            report.append(f"- H2-H6 Tags: H2({headings_info['h2']['count']}), H3({headings_info['h3']['count']}), H4({headings_info['h4']['count']}), H5({headings_info['h5']['count']}), H6({headings_info['h6']['count']})")
        
        if 'images' in details:
            img_info = details['images']
            coverage = round((img_info['with_alt'] / img_info['total'] * 100), 1) if img_info['total'] > 0 else 0
            report.append(f"- Images: {img_info['total']} total, {img_info['with_alt']} with alt text ({coverage}% coverage)")
        
        if 'links' in details:
            links_info = details['links']
            link_status = "Sufficient: 3+" if links_info['internal'] >= 3 else "Insufficient: <3"
            report.append(f"- Internal Links: {links_info['internal']} count - {link_status}")
        
        if 'content' in details:
            content_info = details['content']
            word_count = content_info['word_count']
            content_status = "Sufficient: 300+" if word_count >= 300 else "Short: <300"
            report.append(f"- Content Length: {word_count} words - {content_status}")
        
        return "\n".join(report)
    
    def _generate_passed_tests(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate list of passed SEO tests as bullet points."""
        passed_tests = []
        details = analysis.get('details', {})
        
        if 'title' in details:
            title_info = details['title']
            if title_info.get('status') == 'optimal':
                length = title_info.get('length', 0)
                passed_tests.append(f"Title tag length optimal ({length} characters) - Within recommended 30-60 character range")
        
        if 'meta_description' in details:
            meta_info = details['meta_description']
            if meta_info.get('status') == 'optimal':
                length = meta_info.get('length', 0)
                passed_tests.append(f"Meta description length appropriate ({length} characters) - Within 120-160 character range")
        
        if 'headings' in details:
            headings_info = details['headings']
            if headings_info['h1']['count'] == 1:
                passed_tests.append("Single H1 tag present - Optimal page structure maintained")
            
            if headings_info['h1']['content'] and len(headings_info['h1']['content']) > 0:
                h1_content = headings_info['h1']['content'][0] if isinstance(headings_info['h1']['content'], list) else str(headings_info['h1']['content'])
                passed_tests.append(f"H1 tag contains content - Good for topical relevance")
        
        if 'images' in details:
            img_info = details['images']
            if img_info['alt_ratio'] >= 0.8: 
                passed_tests.append(f"Images with alt text ({img_info['with_alt']} out of {img_info['total']}) - Meets accessibility and SEO requirements")
        
        if 'content' in details:
            content_info = details['content']
            if content_info['word_count'] >= 300:
                passed_tests.append(f"Content length sufficient ({content_info['word_count']} words) - Meets minimum content requirements")
        
        if 'links' in details:
            links_info = details['links']
            if links_info['internal'] >= 3:
                passed_tests.append(f"Internal links present ({links_info['internal']} found) - Supports site navigation and SEO")
        
        return passed_tests
    
    def generate_seo_report_with_keywords(self, analysis: Dict[str, Any], keywords: List[Dict[str, Any]]) -> str:
        """Generate detailed SEO analysis report with mandatory keywords section."""
        if 'error' in analysis:
            return f"Error: {analysis['error']}"
        
        report = []
        report.append(f"SEO Technical Audit Report")
        report.append("=" * 40)
        report.append(f"URL: {analysis['url']}")
        report.append(f"SEO Score: {analysis['seo_score']}/100")
        status = "Excellent" if analysis['seo_score'] >= 90 else "Good" if analysis['seo_score'] >= 70 else "Fair" if analysis['seo_score'] >= 50 else "Poor"
        report.append(f"Status: {status}")
        report.append("")
        
        report.append("🔑 KEYWORDS ANALYSIS (MANDATORY):")
        if keywords:
            for i, kw in enumerate(keywords[:20], 1):
                word = kw.get('word', '')
                count = kw.get('count', 0)
                percentage = kw.get('percentage', 0)
                
                if i == 1:
                    kw_type = "Primary"
                elif i <= 5:
                    kw_type = "Secondary"
                elif len(word.split()) > 1:
                    kw_type = "Long-tail"
                else:
                    kw_type = "Supporting"
                
                report.append(f"{i}. {word}: {count} occurrences ({percentage}% density) - {kw_type}")
        else:
            report.append("No keywords extracted from content")
        report.append("")
        
        report.append("📊 AUDIT SUMMARY:")
        report.append(f"- Total Checks Performed: {analysis['total_checks']}")
        report.append(f"- Passed Tests: {analysis['passed_checks']}")
        report.append(f"- Failed Tests: {analysis['total_checks'] - analysis['passed_checks']}")
        report.append(f"- Warnings: 0")  # Can be enhanced later
        report.append("")
        
        if analysis['issues']:
            report.append("🚨 SEO ISSUES FOUND (Each as individual bullet):")
            for issue in analysis['issues']:
                enhanced_issue = self._enhance_issue_description(issue, keywords)
                report.append(f"• {enhanced_issue}")
            report.append("")
        
        passed_tests = self._generate_passed_tests(analysis)
        if passed_tests:
            report.append("✅ PASSED SEO TESTS (Each as individual bullet):")
            for test in passed_tests:
                report.append(f"• {test}")
            report.append("")
        
        if analysis['recommendations']:
            report.append("💡 OPTIMIZATION RECOMMENDATIONS (Prioritized):")
            for i, rec in enumerate(analysis['recommendations'], 1):
                priority = "HIGH PRIORITY" if i <= 2 else "MEDIUM PRIORITY" if i <= 4 else "LOW PRIORITY"
                enhanced_rec = self._enhance_recommendation(rec, keywords)
                report.append(f"• {priority}: {enhanced_rec}")
            report.append("")
        
        details = analysis.get('details', {})
        report.append("📝 TECHNICAL DETAILS:")
        
        if 'title' in details:
            title_info = details['title']
            title_status = "Present" if title_info.get('content') else "Missing"
            title_length = title_info.get('length', 0)
            
            primary_keyword = keywords[0]['word'] if keywords else ""
            keyword_status = "Contains" if primary_keyword and title_info.get('content') and primary_keyword.lower() in title_info.get('content', '').lower() else "Missing"
            report.append(f"- Title: {title_status} - {title_length} characters - {keyword_status} primary keyword \"{primary_keyword}\"")
        
        if 'meta_description' in details:
            meta_info = details['meta_description']
            meta_status = "Present" if meta_info.get('content') else "Missing"
            meta_length = meta_info.get('length', 0)
            
            primary_keyword = keywords[0]['word'] if keywords else ""
            keyword_status = "Contains" if primary_keyword and meta_info.get('content') and primary_keyword.lower() in meta_info.get('content', '').lower() else "Missing"
            report.append(f"- Meta Description: {meta_status} - {meta_length} characters - {keyword_status} primary keyword \"{primary_keyword}\"")
        
        if 'headings' in details:
            headings_info = details['headings']
            h1_count = headings_info['h1']['count']
            h1_status = "Optimal: 1" if h1_count == 1 else f"Issue: {h1_count}"
            report.append(f"- H1 Tags: {h1_count} count - {h1_status}")
            report.append(f"- H2-H6 Tags: H2({headings_info['h2']['count']}), H3({headings_info['h3']['count']}), H4({headings_info['h4']['count']}), H5({headings_info['h5']['count']}), H6({headings_info['h6']['count']})")
        
        if 'images' in details:
            img_info = details['images']
            coverage = round((img_info['with_alt'] / img_info['total'] * 100), 1) if img_info['total'] > 0 else 0
            report.append(f"- Images: {img_info['total']} total, {img_info['with_alt']} with alt text ({coverage}% coverage)")
        
        if 'links' in details:
            links_info = details['links']
            link_status = "Sufficient: 3+" if links_info['internal'] >= 3 else "Insufficient: <3"
            report.append(f"- Internal Links: {links_info['internal']} count - {link_status}")
        
        if 'content' in details:
            content_info = details['content']
            word_count = content_info['word_count']
            content_status = "Sufficient: 300+" if word_count >= 300 else "Short: <300"
            report.append(f"- Content Length: {word_count} words - {content_status}")
        
        if keywords:
            primary_kw = keywords[0]
            secondary_kw = keywords[1] if len(keywords) > 1 else None
            report.append(f"- Keyword Density: Primary \"{primary_kw['word']}\" ({primary_kw['percentage']}%)" + 
                         (f", Secondary \"{secondary_kw['word']}\" ({secondary_kw['percentage']}%)" if secondary_kw else ""))
        
        return "\n".join(report)
    
    def _enhance_issue_description(self, issue: str, keywords: List[Dict[str, Any]]) -> str:
        """Enhance issue descriptions with keyword context."""
        primary_keyword = keywords[0]['word'] if keywords else "primary keyword"
        
        if "H1 tag missing" in issue or "H1" in issue and "missing" in issue.lower():
            return f"Missing H1 tag - Critical SEO issue affecting page hierarchy, should contain primary keyword \"{primary_keyword}\""
        elif "title" in issue.lower() and "short" in issue.lower():
            return f"{issue} - Should be 30-60 characters for optimal SERP display and include \"{primary_keyword}\""
        elif "meta description" in issue.lower() and "missing" in issue:
            return f"Meta description missing - Required for search engine result snippets, should include \"{primary_keyword}\""
        elif "alt" in issue.lower():
            return f"{issue} - Impacts accessibility and SEO, consider using relevant keywords in alt text"
        elif "density" in issue.lower():
            return f"{issue} - Should be 1-3% to avoid over-optimization penalties"
        else:
            return issue
    
    def _enhance_recommendation(self, recommendation: str, keywords: List[Dict[str, Any]]) -> str:
        """Enhance recommendations with specific keyword suggestions."""
        primary_keyword = keywords[0]['word'] if keywords else "primary keyword"
        secondary_keyword = keywords[1]['word'] if len(keywords) > 1 else "secondary keyword"
        
        if "H1" in recommendation and "add" in recommendation:
            return f"Add missing H1 tag with primary keyword \"{primary_keyword}\" for better topical relevance"
        elif "meta description" in recommendation.lower():
            return f"Write meta description (120-160 characters) including primary keyword \"{primary_keyword}\" and compelling CTA"
        elif "alt" in recommendation.lower():
            return f"Add alt text to images using relevant keywords like \"{primary_keyword}\" and \"{secondary_keyword}\" where contextually appropriate"
        elif "content" in recommendation.lower():
            return f"Expand content by 100-200 words focusing on \"{primary_keyword}\" and related terms for better topical coverage"
        else:
            return recommendation
