# seo_crawler.py - improved version

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random
from requests.exceptions import RequestException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SEOCrawler:
    def __init__(self, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'):
        """Initialize the crawler with more realistic user agent."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        })
        self.visited_urls = set()
        self.pages_data = {}
        self.max_pages = 10
        self.timeout = 15  # Increased timeout
        
    def crawl(self, start_url):
        """Crawl the website starting from the given URL, collecting up to 10 pages."""
        logger.info(f"Starting crawl from: {start_url}")

        def normalize_url(url):
            url = url.rstrip('/')  # Remove trailing slash
            url = url.split('#')[0]  # Remove fragments
            url = url.split('?')[0]  # Remove query parameters
            return url.lower()  # Case normalization (if server is case-insensitive)

        if start_url.endswith('/'):
            start_url = start_url[:-1]
        parsed_url = urlparse(start_url)

        # Normalize the start URL
        parsed_url = urlparse(start_url)
        base_domain = parsed_url.netloc
        if not base_domain:
            logger.error("Invalid URL provided")
            return {}
        
        # Ensure the URL has a scheme
        if not parsed_url.scheme:
            start_url = 'https://' + start_url
            
        # Queue for BFS crawling
        queue = [start_url]
        retry_count = 0
        max_retries = 3
        
        while queue and len(self.pages_data) < self.max_pages:
            current_url = queue.pop(0)
            
            # Skip if already visited
            if current_url in self.visited_urls:
                continue
                
            self.visited_urls.add(current_url)
            
            try:
                # Respect crawl rate (be a good bot)
                time.sleep(random.uniform(2.0, 3.0))
                
                logger.info(f"Crawling: {current_url}")
                response = self.session.get(current_url, timeout=self.timeout)
                
                # Skip non-HTML responses and failed requests
                if not response.ok:
                    logger.warning(f"Got status code {response.status_code} for {current_url}")
                    continue
                    
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    logger.warning(f"Not an HTML page: {current_url}")
                    continue
                    
                # Parse the HTML content
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Store the page data
                self.pages_data[current_url] = html_content
                logger.info(f"Successfully crawled page {len(self.pages_data)}: {current_url}")
                
                # Find all links on the page
                if len(self.pages_data) < self.max_pages:
                    links = soup.find_all('a', href=True)
                    logger.info(f"Found {len(links)} links on {current_url}")
                    
                    for link in links:
                        href = link['href']
                        full_url = urljoin(current_url, href)
                        full_url = normalize_url(full_url)  # <-- ADD THIS

                        
                        # Only follow links to the same domain
                        parsed_href = urlparse(full_url)
                        if parsed_href.netloc == base_domain and full_url not in self.visited_urls:
                            # Exclude common non-content URLs
                            if not self._should_exclude(full_url):
                                queue.append(full_url)
                
            except RequestException as e:
                logger.error(f"Error crawling {current_url}: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f"Retrying... Attempt {retry_count}/{max_retries}")
                    queue.insert(0, current_url)  # Put back at front of queue
                    time.sleep(5)  # Wait before retry
                else:
                    logger.error(f"Max retries exceeded for {current_url}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
        
        if not self.pages_data:
            logger.warning("Could not crawl any pages. Try a different website or check your connection.")
        else:
            logger.info(f"Crawl complete. Collected {len(self.pages_data)} pages.")
        
        return self.pages_data
    
    def _should_exclude(self, url):
        """Check if URL should be excluded from crawling."""
        # Exclude common file types, admin areas, etc.
        exclude_patterns = [
            '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.css', '.js',
            '/wp-admin/', '/wp-login.php', '/cart', '/checkout',
            '/login', '/logout', '/admin', '/feed/', '/rss/',
            '#', 'javascript:', 'mailto:', 'tel:', 'share=', 'popup'
        ]
        
        lower_url = url.lower()
        return any(pattern in lower_url for pattern in exclude_patterns)


if __name__ == "__main__":
    # Test the crawler
    crawler = SEOCrawler()
    
    # Suggest more crawler-friendly sites
    print("Recommended test sites: blog.python.org, example.com, httpbin.org")
    url_to_crawl = input("Enter the website URL to crawl: ")
    
    results = crawler.crawl(url_to_crawl)
    print(f"Successfully crawled {len(results)} pages.")
    
    # Print the first few URLs crawled
    if results:
        print("\nCrawled URLs:")
        for i, url in enumerate(list(results.keys())[:5]):
            print(f"{i+1}. {url}")
        
        if len(results) > 5:
            print(f"...and {len(results) - 5} more")