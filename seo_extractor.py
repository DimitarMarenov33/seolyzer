# seo_extractor.py

from bs4 import BeautifulSoup
import re
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SEOExtractor:
    def __init__(self):
        """Initialize the SEO data extractor."""
        pass
        
    def extract_seo_data(self, url, html_content):
        """Extract SEO data from HTML content."""
        logger.info(f"Extracting SEO data from: {url}")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract data
        data = {
            'url': url,
            'meta_title': self._extract_meta_title(soup),
            'meta_description': self._extract_meta_description(soup),
            'h1_tags': self._extract_h1_tags(soup),
            'word_count': self._calculate_word_count(soup),
            'structured_data': self._extract_structured_data(soup)
        }
        
        logger.info(f"Extraction complete for: {url}")
        return data
    
    def _extract_meta_title(self, soup):
        """Extract meta title from the page."""
        # Try title tag first
        title_tag = soup.title
        title = title_tag.string.strip() if title_tag else None
        
        # If no title tag, try meta title
        if not title:
            meta_title = soup.find('meta', attrs={'name': 'title'})
            if meta_title and meta_title.get('content'):
                title = meta_title['content'].strip()
                
        return title or "No title found"
    
    def _extract_meta_description(self, soup):
        """Extract meta description from the page."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else None
        return description or "No meta description found"
    
    def _extract_h1_tags(self, soup):
        """Extract H1 tags from the page."""
        h1_elements = soup.find_all('h1')
        h1_contents = [h1.get_text().strip() for h1 in h1_elements]
        
        # Also check for the count - multiple H1s are an SEO issue
        h1_count = len(h1_contents)
        
        return {
            'count': h1_count,
            'contents': h1_contents if h1_contents else ["No H1 tag found"]
        }
    
    def _calculate_word_count(self, soup):
        """Calculate approximate word count of the main content."""
        # Remove scripts, styles, and other non-content elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.extract()
        
        # Get the text and normalize spaces
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Count words
        words = text.split()
        return len(words)
    
    def _extract_structured_data(self, soup):
        """Extract structured data from the page."""
        structured_data = {
            'json_ld': self._extract_json_ld(soup),
            'microdata': self._check_microdata(soup),
            'rdfa': self._check_rdfa(soup)
        }
        
        # Also provide a summary of what was found
        found_types = []
        if structured_data['json_ld']:
            found_types.append('JSON-LD')
        if structured_data['microdata']:
            found_types.append('Microdata')
        if structured_data['rdfa']:
            found_types.append('RDFa')
            
        structured_data['summary'] = found_types if found_types else ["No structured data found"]
        
        return structured_data
    
    def _extract_json_ld(self, soup):
        """Extract JSON-LD structured data."""
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        result = []
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                # Just extract the @type for summary purposes
                if isinstance(data, dict) and '@type' in data:
                    result.append(data['@type'])
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and '@type' in item:
                            result.append(item['@type'])
            except (json.JSONDecodeError, AttributeError):
                pass
                
        return result
    
    def _check_microdata(self, soup):
        """Check for presence of Microdata."""
        # Look for itemscope, itemtype attributes
        elements_with_itemscope = soup.find_all(attrs={'itemscope': True})
        
        microdata_types = []
        for element in elements_with_itemscope:
            if element.get('itemtype'):
                microdata_types.append(element['itemtype'])
                
        return microdata_types
    
    def _check_rdfa(self, soup):
        """Check for presence of RDFa."""
        # Look for typeof, property attributes
        elements_with_typeof = soup.find_all(attrs={'typeof': True})
        
        rdfa_types = []
        for element in elements_with_typeof:
            if element.get('typeof'):
                rdfa_types.append(element['typeof'])
                
        return rdfa_types


if __name__ == "__main__":
    # This is just for testing the extractor directly
    import requests
    
    url = input("Enter a URL to extract SEO data: ")
    response = requests.get(url)
    
    if response.ok:
        extractor = SEOExtractor()
        seo_data = extractor.extract_seo_data(url, response.text)
        
        # Print formatted results
        print("\n===== SEO Data Extraction Results =====")
        print(f"URL: {seo_data['url']}")
        print(f"Meta Title: {seo_data['meta_title']}")
        print(f"Meta Description: {seo_data['meta_description']}")
        print(f"H1 Tags ({seo_data['h1_tags']['count']}): {', '.join(seo_data['h1_tags']['contents'])}")
        print(f"Word Count: {seo_data['word_count']}")
        print(f"Structured Data: {', '.join(seo_data['structured_data']['summary'])}")
    else:
        print(f"Error: Could not fetch URL (Status code: {response.status_code})")