  SEOlyzer - AI-Powered SEO Audit Tool

  🌐 Live Demo
🚀 **Try SEOlyzer**: https://seolyzer-production.up.railway.app

An autonomous AI-powered agent that performs comprehensive SEO audits on websites and generates actionable recommendations in natural language.

   🚀 Features

-  Autonomous Website Crawling : Crawls up to 10 pages automatically
-  Comprehensive SEO Analysis : Extracts meta titles, descriptions, H1 tags, word counts, and structured data
-  AI-Powered Recommendations : Uses OpenAI GPT-4o-mini to generate actionable SEO insights
-  Beautiful Reports : Generates stunning HTML reports with futuristic design
-  Real-Time Progress : Live progress tracking during analysis
-  Professional UI : Modern web interface with animations and responsive design

   🛠 Tech Stack

-  Backend : Python Flask
-  Web Crawling : Requests + BeautifulSoup
-  AI Analysis : OpenAI GPT-4o-mini API
-  Frontend : HTML/CSS/JavaScript with custom animations
-  Template Engine : Jinja2
-  Styling : Custom CSS with futuristic design elements

   📋 Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt

   🚀 Installation & Setup

1.  Clone the repository 
   ```bash
   git clone <repository-url>
   cd seolyzer
   ```

2.  Create virtual environment 
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    On macOS/Linux
     or
   .venv\Scripts\activate    On Windows
   ```

3.  Install dependencies 
   ```bash
   pip install -r requirements.txt
   ```

4.  Set up OpenAI API key 
   ```bash
     Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

5.  Run the application 
   ```bash
   python app.py
   ```

6.  Access the web interface 
   Open your browser and navigate to `http://localhost:8000`

   📖 How to Use

1.  Start Analysis : Enter a website URL in the web interface
2.  Monitor Progress : Watch real-time progress as SEOlyzer:
   - Crawls up to 10 pages of the website
   - Extracts SEO data from each page
   - Generates AI-powered recommendations
3.  View Results : Access the beautiful HTML report with:
   - Overall website score
   - Individual page scores
   - Detailed SEO recommendations
   - Technical improvement suggestions

   🔧 Core Components

- `app.py` - Flask web application and API endpoints
- `seo_crawler.py` - Website crawling functionality
- `seo_extractor.py` - SEO data extraction from HTML
- `seo_recommendation.py` - OpenAI integration for recommendations
- `seo_report_generator.py` - HTML report generation with styling
- `templates/index.html` - Web interface frontend

   🎯 Key Assumptions

-  Website Accessibility : Target websites are publicly accessible and don't require authentication
-  Crawl Politeness : Implements rate limiting (1-3 seconds between requests) to be respectful to target servers
-  Domain Restriction : Only crawls pages within the same domain to stay focused
-  Content Types : Focuses on HTML pages and excludes PDFs, images, and other file types
-  Language : Works best with English content but handles multilingual sites
-  API Limits : Uses OpenAI API efficiently with token limits per request

   💰 Cost Considerations

-  OpenAI API Usage : Approximately $0.007 per website analysis (very affordable)
-  No other external costs : All other components are free and open-source

   🌟 Sample Output

The tool generates comprehensive reports including:
-  Overall SEO Score : Averaged across all analyzed pages
-  Page-by-Page Analysis : Individual scores and recommendations
-  Actionable Insights : Specific improvements for meta tags, content, and technical SEO
-  Quick Wins : Immediate actions to improve rankings

   🔮 Future Enhancements

- Support for larger websites (configurable page limits)
- Additional SEO metrics (Core Web Vitals, accessibility)
- Competitor analysis features
- Historical tracking and comparison
- API endpoints for integration with other tools

   📄 License

This project is created as part of a technical assessment for Seeders Agency.

---

*Built with ❤️ for the Seeders AI Developer Assessment*
