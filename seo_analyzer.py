# seo_analyzer.py
#sk-eff22960284b4ae78a7606c9441a45bc

from seo_crawler import SEOCrawler
from seo_extractor import SEOExtractor
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SEOAnalyzer:
    def __init__(self):
        """Initialize the SEO analyzer with crawler and extractor."""
        self.crawler = SEOCrawler()
        self.extractor = SEOExtractor()
        self.results = {}
        
    def analyze(self, url):
        """Run a complete SEO analysis on the given URL."""
        logger.info(f"Starting SEO analysis for: {url}")
        start_time = time.time()
        
        # Step 1: Crawl the website
        crawled_pages = self.crawler.crawl(url)
        
        if not crawled_pages:
            logger.error("Crawling failed. No pages were collected.")
            return None
            
        # Step 2: Extract SEO data from each page
        for page_url, html_content in crawled_pages.items():
            logger.info(f"Analyzing SEO data for: {page_url}")
            seo_data = self.extractor.extract_seo_data(page_url, html_content)
            self.results[page_url] = seo_data
        
        elapsed_time = time.time() - start_time
        logger.info(f"SEO analysis complete. Analyzed {len(self.results)} pages in {elapsed_time:.2f} seconds.")
        
        return self.results
    
    def save_results(self, filename='seo_analysis_results.json'):
        """Save the analysis results to a JSON file."""
        if not self.results:
            logger.warning("No results to save.")
            return False
            
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
            
        logger.info(f"Results saved to {filename}")
        return True


if __name__ == "__main__":
    analyzer = SEOAnalyzer()
    url_to_analyze = input("Enter the website URL to analyze: ")
    
    results = analyzer.analyze(url_to_analyze)
    
    if results:
        # Save results to file
        analyzer.save_results()
        
        # Print summary
        print("\n===== SEO Analysis Summary =====")
        print(f"Total pages analyzed: {len(results)}")
        
        print("\nPage Titles:")
        for url, data in results.items():
            print(f"- {data['meta_title']} ({url})")