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

"""Web crawling utilities for SEO analysis."""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Any
import re
from collections import Counter


def crawl_webpage(url: str) -> Dict[str, Any]:
    """
    Web sayfasını crawl eder ve HTML içeriğini analiz eder.
    
    Args:
        url: Analiz edilecek web sayfasının URL'i
        
    Returns:
        Web sayfası analiz sonuçları içeren dictionary
    """
    try:
        # Web sayfasını al
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTML'i parse et
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Analiz sonuçları
        analysis = {
            'url': url,
            'title': get_page_title(soup),
            'meta_description': get_meta_description(soup),
            'headings': extract_headings(soup),
            'images': extract_images(soup, url),
            'paragraphs': extract_paragraphs(soup),
            'links': extract_links(soup, url),
            'keywords': extract_keywords(soup),
            'html_content': str(soup),
            'text_content': soup.get_text(),
            'word_count': len(soup.get_text().split()),
            'status_code': response.status_code
        }
        
        return analysis
        
    except requests.RequestException as e:
        return {
            'error': f'Error fetching web page: {str(e)}',
            'url': url,
            'status_code': None
        }
    except Exception as e:
        return {
            'error': f'Error during analysis: {str(e)}',
            'url': url,
            'status_code': None
        }


def get_page_title(soup: BeautifulSoup) -> Optional[str]:
    """Sayfanın title etiketini döndürür."""
    title_tag = soup.find('title')
    return title_tag.get_text().strip() if title_tag else None


def get_meta_description(soup: BeautifulSoup) -> Optional[str]:
    """Meta description etiketini döndürür."""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        return meta_desc.get('content', '').strip()
    return None


def extract_headings(soup: BeautifulSoup) -> Dict[str, List[str]]:
    """H1, H2, H3, H4, H5, H6 etiketlerini çıkarır."""
    headings = {}
    for i in range(1, 7):
        tag_name = f'h{i}'
        tags = soup.find_all(tag_name)
        headings[tag_name] = [tag.get_text().strip() for tag in tags]
    return headings


def extract_images(soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
    """IMG etiketlerini ve özelliklerini çıkarır."""
    images = []
    img_tags = soup.find_all('img')
    
    for img in img_tags:
        src = img.get('src', '')
        if src:
            # Relative URL'leri absolute'a çevir
            if src.startswith('/') or not urlparse(src).netloc:
                src = urljoin(base_url, src)
        
        images.append({
            'src': src,
            'alt': img.get('alt', ''),
            'title': img.get('title', ''),
            'width': img.get('width', ''),
            'height': img.get('height', '')
        })
    
    return images


def extract_paragraphs(soup: BeautifulSoup) -> List[str]:
    paragraphs = soup.find_all('p')
    return [p.get_text().strip() for p in paragraphs if p.get_text().strip()]


def extract_links(soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
    links = []
    a_tags = soup.find_all('a', href=True)
    
    for link in a_tags:
        href = link.get('href', '')
        if href:
            # Relative URL'leri absolute'a çevir
            if href.startswith('/') or not urlparse(href).netloc:
                href = urljoin(base_url, href)
        
        links.append({
            'href': href,
            'text': link.get_text().strip(),
            'title': link.get('title', '')
        })
    
    return links


def extract_keywords(soup: BeautifulSoup, min_length: int = 3, top_n: int = 20) -> List[Dict[str, Any]]:
    """
    Sayfadan anahtar kelimeleri çıkarır ve sıklıklarını hesaplar.
    
    Args:
        soup: BeautifulSoup objesi
        min_length: Minimum kelime uzunluğu
        top_n: En çok kullanılan kaç kelime döndürülecek
        
    Returns:
        Anahtar kelime listesi (kelime, sıklık)
    """
    for script in soup(["script", "style"]):
        script.decompose()
    
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    
    words = re.findall(r'\b[a-zA-ZğüşıöçĞÜŞİÖÇ]+\b', text)
    words = [word for word in words if len(word) >= min_length]
    
    # Comprehensive stop words list to filter out common, non-meaningful words
    stop_words = {
        # English articles, prepositions, conjunctions
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
        'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 
        'after', 'above', 'below', 'between', 'among', 'within', 'without',
        
        # English pronouns and determiners
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs',
        'this', 'that', 'these', 'those', 'some', 'any', 'each', 'every', 'all', 'both', 'few', 'many',
        
        # English common verbs (including the problematic ones mentioned)
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
        'do', 'does', 'did', 'doing', 'will', 'would', 'could', 'should', 'may', 'might', 
        'must', 'can', 'get', 'got', 'getting', 'go', 'goes', 'went', 'going', 'come', 'came', 
        'coming', 'see', 'saw', 'seen', 'seeing', 'know', 'knew', 'known', 'knowing',
        'think', 'thought', 'thinking', 'take', 'took', 'taken', 'taking', 'make', 'made', 
        'making', 'give', 'gave', 'given', 'giving', 'use', 'used', 'using', 'find', 'found', 
        'finding', 'tell', 'told', 'telling', 'ask', 'asked', 'asking', 'work', 'worked', 'working',
        'try', 'tried', 'trying', 'call', 'called', 'calling', 'need', 'needed', 'needing',
        'feel', 'felt', 'feeling', 'become', 'became', 'becoming', 'leave', 'left', 'leaving',
        'put', 'putting', 'mean', 'meant', 'meaning', 'keep', 'kept', 'keeping', 'let', 'letting',
        'begin', 'began', 'begun', 'beginning', 'seem', 'seemed', 'seeming', 'help', 'helped', 'helping',
        'talk', 'talked', 'talking', 'turn', 'turned', 'turning', 'start', 'started', 'starting',
        'show', 'showed', 'shown', 'showing', 'hear', 'heard', 'hearing', 'play', 'played', 'playing',
        'run', 'ran', 'running', 'move', 'moved', 'moving', 'live', 'lived', 'living', 'believe', 
        'believed', 'believing', 'hold', 'held', 'holding', 'bring', 'brought', 'bringing',
        'happen', 'happened', 'happening', 'write', 'wrote', 'written', 'writing', 'provide', 
        'provided', 'providing', 'sit', 'sat', 'sitting', 'stand', 'stood', 'standing',
        'lose', 'lost', 'losing', 'pay', 'paid', 'paying', 'meet', 'met', 'meeting',
        'include', 'included', 'including', 'continue', 'continued', 'continuing', 'set', 'setting',
        'learn', 'learned', 'learnt', 'learning', 'change', 'changed', 'changing', 'lead', 'led', 'leading',
        'understand', 'understood', 'understanding', 'watch', 'watched', 'watching', 'follow', 'followed', 'following',
        'stop', 'stopped', 'stopping', 'create', 'created', 'creating', 'speak', 'spoke', 'spoken', 'speaking',
        'read', 'reading', 'allow', 'allowed', 'allowing', 'add', 'added', 'adding', 'spend', 'spent', 'spending',
        'grow', 'grew', 'grown', 'growing', 'open', 'opened', 'opening', 'walk', 'walked', 'walking',
        'win', 'won', 'winning', 'offer', 'offered', 'offering', 'remember', 'remembered', 'remembering',
        'love', 'loved', 'loving', 'consider', 'considered', 'considering', 'appear', 'appeared', 'appearing',
        'buy', 'bought', 'buying', 'wait', 'waited', 'waiting', 'serve', 'served', 'serving',
        'die', 'died', 'dying', 'send', 'sent', 'sending', 'expect', 'expected', 'expecting',
        'build', 'built', 'building', 'stay', 'stayed', 'staying', 'fall', 'fell', 'fallen', 'falling',
        'cut', 'cutting', 'reach', 'reached', 'reaching', 'kill', 'killed', 'killing', 'remain', 'remained', 'remaining',
        
        # English common adverbs and adjectives
        'not', 'no', 'yes', 'so', 'just', 'now', 'then', 'here', 'there', 'where', 'when', 'why', 'how',
        'what', 'who', 'which', 'whose', 'whom', 'very', 'too', 'also', 'well', 'still', 'only', 'even',
        'back', 'more', 'most', 'other', 'another', 'such', 'own', 'out', 'way', 'time', 'new', 'first',
        'last', 'long', 'great', 'little', 'old', 'right', 'big', 'high', 'different', 'small', 'large',
        'next', 'early', 'young', 'important', 'few', 'public', 'bad', 'same', 'able', 'good', 'best',
        'better', 'worse', 'worst', 'much', 'many', 'less', 'least', 'enough', 'quite', 'rather',
        'pretty', 'really', 'actually', 'certainly', 'probably', 'perhaps', 'maybe', 'almost', 'always',
        'never', 'sometimes', 'often', 'usually', 'again', 'once', 'twice', 'ever', 'already', 'yet',
        
        # Common website/business terms that are usually not meaningful keywords
        'home', 'about', 'contact', 'page', 'website', 'site', 'web', 'click', 'here', 'link', 'links',
        'menu', 'navigation', 'nav', 'header', 'footer', 'sidebar', 'content', 'main', 'section',
        'article', 'post', 'blog', 'news', 'read', 'more', 'less', 'view', 'show', 'hide', 'toggle',
        'button', 'form', 'input', 'submit', 'search', 'find', 'results', 'result', 'page', 'pages',
        'next', 'previous', 'prev', 'first', 'last', 'login', 'logout', 'sign', 'register', 'account',
        'user', 'users', 'admin', 'administrator', 'settings', 'options', 'preferences', 'profile',
        'dashboard', 'panel', 'control', 'manage', 'management', 'system', 'data', 'information', 'info',
        'details', 'description', 'title', 'name', 'email', 'password', 'username', 'date', 'time',
        'category', 'categories', 'tag', 'tags', 'archive', 'archives', 'recent', 'popular', 'featured',
        'related', 'similar', 'share', 'social', 'facebook', 'twitter', 'instagram', 'linkedin',
        'youtube', 'google', 'apple', 'microsoft', 'amazon', 'meta', 'company', 'business', 'service',
        'services', 'product', 'products', 'solution', 'solutions', 'team', 'staff', 'member', 'members',
        'client', 'clients', 'customer', 'customers', 'support', 'help', 'faq', 'privacy', 'policy',
        'terms', 'conditions', 'legal', 'copyright', 'rights', 'reserved', 'inc', 'ltd', 'llc', 'corp',
        'corporation', 'company', 'group', 'international', 'global', 'worldwide', 'national', 'local','cookies','powered','powered by',
        'privacy policy','terms of service','terms of use','disclaimer','contact us','about us','our services',
        'our products','our team','our company','our business','our website','our blog','our news','our articles','our posts','our pages',
        'our content','our information','our details','our description','our title','our name','our email','our password','our username',
        'our date','our time','our category','our categories','our tag','our tags','our archive','our archives','our recent','our popular',
        'our featured','our related','our similar','our share','our social','our facebook','our twitter','our instagram','our linkedin',
        'our youtube','our google','our apple','our microsoft','our amazon','our meta','our company','our business','our service',
        'our services','our product','our products','our solution','our solutions','our team','our staff','our member','our members',
        'our client','our clients','our customer','our customers','our support','our help','our faq','our privacy','our policy',
        'our terms','our conditions','our legal','our copyright','our rights','our reserved','our inc','our ltd','our llc','our corp',
        'our corporation','our group','our international','our global','our worldwide','our national','our local'
    }
    
    filtered_words = [word for word in words if word not in stop_words]
    
    # Sıklık hesapla
    word_counts = Counter(filtered_words)
    
    # En çok kullanılan kelimeleri döndür
    top_keywords = []
    for word, count in word_counts.most_common(top_n):
        percentage = (count / len(filtered_words)) * 100 if filtered_words else 0
        top_keywords.append({
            'word': word,
            'count': count,
            'percentage': round(percentage, 2)
        })
    
    return top_keywords


def calculate_keyword_density(text: str, keyword: str) -> float:
    """Belirli bir anahtar kelimenin yoğunluğunu hesaplar."""
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    # Toplam kelime sayısı
    words = re.findall(r'\b\w+\b', text_lower)
    total_words = len(words)
    
    if total_words == 0:
        return 0.0
    
    # Anahtar kelime sayısı
    keyword_count = text_lower.count(keyword_lower)
    
    # Yoğunluk hesapla (yüzde olarak)
    density = (keyword_count / total_words) * 100
    return round(density, 2)
