# seo_recommendation.py (OpenAI version - Modern API)

from openai import OpenAI
import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SEORecommendationGenerator:
    def __init__(self, api_key=None):
        """Initialize with OpenAI API key."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            logger.warning("No OpenAI API key provided. Set OPENAI_API_KEY environment variable.")
            self.client = None
        else:
            # Initialize OpenAI client with modern API
            self.client = OpenAI(api_key=self.api_key)
            logger.info("Using OpenAI GPT-4o-mini for SEO recommendations")
            
    def generate_recommendations(self, seo_data):
        """Generate SEO recommendations using OpenAI."""
        if not self.client:
            logger.error("Cannot generate recommendations: No OpenAI API key provided.")
            return {"error": "API key not configured"}
            
        try:
            prompt = self._create_prompt(seo_data)
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cost-effective
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert SEO consultant. Provide concise, actionable recommendations. Structure your response with: **Overall Score**, **Critical Issues**, **Content Recommendations**, and **Technical Improvements**. Use **bold** formatting for section headers."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800  # Keep responses focused
            )
            
            recommendations = response.choices[0].message.content
            logger.info(f"Successfully generated recommendations for {seo_data['url']}")
            return {"recommendations": recommendations}
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {"error": str(e)}
            
    def _create_prompt(self, seo_data):
        """Create prompt for OpenAI."""
        prompt = f"""
Analyze this webpage's SEO and provide recommendations:

URL: {seo_data['url']}
Page Title: {seo_data['meta_title']}
Meta Description: {seo_data['meta_description']}
H1 Tags ({seo_data['h1_tags']['count']}): {", ".join(seo_data['h1_tags']['contents'])}
Word Count: {seo_data['word_count']}
Structured Data: {", ".join(seo_data['structured_data']['summary'])}

Provide:
1. **Overall Score:** Give a score from 0-100
2. **Critical Issues:** Top 3 critical issues to fix immediately
3. **Content Recommendations:** Content optimization suggestions
4. **Technical Improvements:** Technical SEO improvements
5. **Quick Win:** One actionable tip for immediate improvement

Be specific and actionable. Use **bold** formatting for section headers.
"""
        return prompt

    def process_website_data(self, seo_data_dict):
        """Process all pages from a website."""
        results = {}
        
        for url, page_data in seo_data_dict.items():
            logger.info(f"Generating recommendations for: {url}")
            page_recommendations = self.generate_recommendations(page_data)
            results[url] = {
                "seo_data": page_data,
                "recommendations": page_recommendations.get("recommendations", "Error generating recommendations")
            }
            
        return results