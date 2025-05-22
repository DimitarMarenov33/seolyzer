# app.py - SEOlyzer Flask Web Application

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
import threading
import time
from datetime import datetime
import logging

# Import your existing SEO analysis modules
from seo_crawler import SEOCrawler
from seo_extractor import SEOExtractor
from seo_recommendation import SEORecommendationGenerator
from seo_report_generator import SEOReportGenerator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Global variable to store analysis status
analysis_status = {}

class SEOAnalysisRunner:
    def __init__(self):
        self.crawler = SEOCrawler()
        self.extractor = SEOExtractor()
        self.recommendation_generator = SEORecommendationGenerator()
        self.report_generator = SEOReportGenerator()
        
    def run_analysis(self, url, analysis_id):
        """Run the complete SEO analysis"""
        try:
            analysis_status[analysis_id] = {
                'status': 'crawling',
                'progress': 10,
                'message': 'Starting website crawl...',
                'start_time': datetime.now()
            }
            
            # Step 1: Crawl the website
            logger.info(f"Starting crawl for {url}")
            crawled_pages = self.crawler.crawl(url)
            
            if not crawled_pages:
                analysis_status[analysis_id] = {
                    'status': 'error',
                    'message': 'Failed to crawl website. Please check the URL.',
                    'progress': 0
                }
                return
                
            analysis_status[analysis_id].update({
                'status': 'extracting',
                'progress': 30,
                'message': f'Crawled {len(crawled_pages)} pages. Extracting SEO data...'
            })
            
            # Step 2: Extract SEO data
            seo_data = {}
            for i, (page_url, html_content) in enumerate(crawled_pages.items()):
                page_data = self.extractor.extract_seo_data(page_url, html_content)
                seo_data[page_url] = page_data
                
                progress = 30 + (i / len(crawled_pages)) * 30
                analysis_status[analysis_id].update({
                    'progress': int(progress),
                    'message': f'Extracting data from page {i+1}/{len(crawled_pages)}'
                })
                
            analysis_status[analysis_id].update({
                'status': 'analyzing',
                'progress': 60,
                'message': 'Generating AI-powered recommendations...'
            })
            
            # Step 3: Generate recommendations
            results_with_recommendations = {}
            for i, (url_key, page_data) in enumerate(seo_data.items()):
                recommendations = self.recommendation_generator.generate_recommendations(page_data)
                results_with_recommendations[url_key] = {
                    "seo_data": page_data,
                    "recommendations": recommendations.get("recommendations", "Error generating recommendations")
                }
                
                progress = 60 + (i / len(seo_data)) * 30
                analysis_status[analysis_id].update({
                    'progress': int(progress),
                    'message': f'Analyzing page {i+1}/{len(seo_data)}'
                })
                
            analysis_status[analysis_id].update({
                'status': 'generating_report',
                'progress': 90,
                'message': 'Generating beautiful report...'
            })
            
            # Step 4: Generate report
            report_filename = f"seolyzer_report_{analysis_id}.html"
            report_path = self.report_generator.generate_html_report(
                results_with_recommendations, 
                report_filename
            )
            
            if report_path:
                analysis_status[analysis_id] = {
                    'status': 'completed',
                    'progress': 100,
                    'message': 'Analysis complete!',
                    'report_path': report_path,
                    'end_time': datetime.now(),
                    'pages_analyzed': len(seo_data)
                }
            else:
                analysis_status[analysis_id] = {
                    'status': 'error',
                    'message': 'Failed to generate report',
                    'progress': 90
                }
                
        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            analysis_status[analysis_id] = {
                'status': 'error',
                'message': f'Analysis failed: {str(e)}',
                'progress': 0
            }

@app.route('/')
def index():
    """Main page with URL input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def start_analysis():
    """Start SEO analysis"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
        
    # Validate URL format
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
        
    # Generate unique analysis ID
    analysis_id = f"analysis_{int(time.time())}"
    
    # Initialize analysis status
    analysis_status[analysis_id] = {
        'status': 'starting',
        'progress': 0,
        'message': 'Initializing analysis...',
        'url': url
    }
    
    # Start analysis in background thread
    analyzer = SEOAnalysisRunner()
    thread = threading.Thread(
        target=analyzer.run_analysis, 
        args=(url, analysis_id)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'analysis_id': analysis_id,
        'status': 'started',
        'message': 'Analysis started successfully'
    })

@app.route('/status/<analysis_id>')
def get_status(analysis_id):
    """Get analysis status"""
    status = analysis_status.get(analysis_id, {
        'status': 'not_found',
        'message': 'Analysis not found'
    })
    return jsonify(status)

@app.route('/report/<analysis_id>')
def view_report(analysis_id):
    """View the generated report"""
    status = analysis_status.get(analysis_id, {})
    
    if status.get('status') != 'completed':
        return redirect(url_for('index'))
        
    report_path = status.get('report_path')
    if report_path and os.path.exists(report_path):
        return send_file(report_path)
    else:
        return "Report not found", 404

@app.route('/download/<analysis_id>')
def download_report(analysis_id):
    """Download the report"""
    status = analysis_status.get(analysis_id, {})
    
    if status.get('status') != 'completed':
        return jsonify({'error': 'Analysis not completed'}), 400
        
    report_path = status.get('report_path')
    if report_path and os.path.exists(report_path):
        return send_file(
            report_path, 
            as_attachment=True, 
            download_name=f"seolyzer_report_{analysis_id}.html"
        )
    else:
        return jsonify({'error': 'Report not found'}), 404

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=8000)