# main.py (updated for OpenAI)

import os
import json
import logging
from seo_crawler import SEOCrawler
from seo_extractor import SEOExtractor
from seo_recommendation import SEORecommendationGenerator
from seo_report_generator import SEOReportGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_seo_analysis(url):
    """Run a complete SEO analysis on the given URL."""
    logger.info("Starting SEO analysis")
    
    # Step 1: Crawl the website
    logger.info("Step 1: Crawling website")
    crawler = SEOCrawler()
    crawled_pages = crawler.crawl(url)
    
    if not crawled_pages:
        logger.error("Crawling failed. Exiting.")
        return
        
    # Step 2: Extract SEO data
    logger.info("Step 2: Extracting SEO data")
    extractor = SEOExtractor()
    seo_data = {}
    
    for page_url, html_content in crawled_pages.items():
        page_data = extractor.extract_seo_data(page_url, html_content)
        seo_data[page_url] = page_data
        
    # Save raw SEO data
    with open("seo_analysis_results.json", "w") as f:
        json.dump(seo_data, f, indent=4)
        
    # Step 3: Generate recommendations
    logger.info("Step 3: Generating SEO recommendations")
    recommendation_generator = SEORecommendationGenerator()
    results_with_recommendations = {}
    
    for url, page_data in seo_data.items():
        recommendations = recommendation_generator.generate_recommendations(page_data)
        results_with_recommendations[url] = {
            "seo_data": page_data,
            "recommendations": recommendations.get("recommendations", "Error generating recommendations")
        }
        
    # Save results with recommendations
    with open("seo_results_with_recommendations.json", "w") as f:
        json.dump(results_with_recommendations, f, indent=4)
        
    # Step 4: Generate report
    logger.info("Step 4: Generating report")
    report_generator = SEOReportGenerator()
    html_report_path = report_generator.generate_html_report(results_with_recommendations)
    
    if html_report_path:
        logger.info(f"HTML report generated: {html_report_path}")
        
    logger.info("SEO analysis complete")
    return html_report_path


if __name__ == "__main__":
    # Check if OpenAI API key is configured
    if not os.getenv("OPENAI_API_KEY"):
        print("OpenAI API key not found in environment variables.")
        api_key = input("Enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Also save to .env file for future runs
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("API key saved to .env file")
    
    # Get the URL to analyze
    url = input("Enter the website URL to analyze: ")
    
    # Run the analysis
    report_path = run_seo_analysis(url)
    
    if report_path:
        print(f"\nAnalysis complete! Report saved to: {report_path}")
        print("Open this file in your browser to view the SEO recommendations.")