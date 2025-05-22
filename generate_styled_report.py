# generate_styled_report.py (updated)

import json
import os
import logging
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_score_from_recommendations(recommendations):
    """Extract a numerical score from recommendations text, with improved robustness."""
    if not recommendations or not isinstance(recommendations, str):
        return 0
        
    # First, look for the most common pattern - "Overall Score: XX" with variations
    score_patterns = [
        r'\*\*Overall Score:?\s*(\d+)[\s/]*\d*\*\*',  # **Overall Score: 40/100**
        r'Overall Score:?\s*(\d+)[\s/]*\d*',          # Overall Score: 40/100
        r'\*\*Overall Score:?\s*(\d+)',               # **Overall Score: 40
        r'Overall Score:?\s*(\d+)',                   # Overall Score: 40
        r'\*\*Score:?\s*(\d+)',                       # **Score: 40  
        r'Score:?\s*(\d+)',                           # Score: 40
        r'SEO Score:?\s*(\d+)',                       # SEO Score: 40
    ]
    
    # Try each pattern until we find a match
    for pattern in score_patterns:
        match = re.search(pattern, recommendations, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                continue
    
    # If no match from specific patterns, try a broader approach
    # Look for any number that appears after words like score/rating
    broader_match = re.search(r'(?:score|rating|assessment).*?(\d+)', recommendations, re.IGNORECASE)
    if broader_match:
        try:
            return int(broader_match.group(1))
        except (ValueError, IndexError):
            pass
    
    # As a fallback, scan for any number between 0-100 with context suggesting it's a score
    fallback_scores = re.findall(r'(\d+)[\s/]*100', recommendations)
    if fallback_scores:
        for score_str in fallback_scores:
            try:
                score = int(score_str)
                if 0 <= score <= 100:  # Validate it's a reasonable score
                    return score
            except ValueError:
                continue
    
    # If all else fails, look for any standalone number between 0-100
    # that might represent a score
    number_matches = re.findall(r'\b(\d{1,3})\b', recommendations)
    for num_str in number_matches:
        try:
            num = int(num_str)
            if 20 <= num <= 100:  # Only consider numbers in a typical score range
                return num
        except ValueError:
            continue
    
    # Default if no score found
    return 40  # Return a reasonable default rather than 0

def format_markdown_to_html(text):
    """Convert markdown-style formatting to HTML."""
    if not text or not isinstance(text, str):
        return text
        
    # Convert **text** to <strong>text</strong>
    formatted_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    return formatted_text

# Create templates directory if it doesn't exist
template_dir = "templates"
if not os.path.exists(template_dir):
    os.makedirs(template_dir)

# Create the new template file
template_path = os.path.join(template_dir, "futuristic_template.html")
with open(template_path, "w") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #0ee3ff;
            --secondary-color: #3d54ff;
            --dark-bg: #0a0a1a;
            --card-bg: #111124;
            --text-color: #e0e0e0;
            --glow-intensity: 5px;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: all 0.3s ease;
        }
        
        body {
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--dark-bg);
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(61, 84, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(14, 227, 255, 0.1) 0%, transparent 50%);
            background-attachment: fixed;
            overflow-x: hidden;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(45deg, 
                          rgba(10, 10, 26, 0.7) 0%,
                          rgba(10, 10, 26, 0.8) 50%, 
                          rgba(10, 10, 26, 0.7) 100%);
            background-size: 400% 400%;
            animation: gradientMovement 15s ease infinite;
        }
        
        @keyframes gradientMovement {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        header {
            background-color: rgba(10, 10, 26, 0.8);
            padding: 40px 0;
            margin-bottom: 40px;
            box-shadow: 0 5px 20px rgba(14, 227, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        /* Header background animation */
        header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, 
                          transparent, 
                          rgba(14, 227, 255, 0.03), 
                          transparent);
            transform: rotate(45deg);
            animation: headerShine 10s linear infinite;
            z-index: 0;
        }
        
        @keyframes headerShine {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }
        
        header .container {
            position: relative;
            z-index: 1;
        }
        
        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 10px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            position: relative;
            display: inline-block;
            text-shadow: 0 0 var(--glow-intensity) rgba(14, 227, 255, 0.5);
            animation: pulsate 3s infinite alternate;
        }
        
        @keyframes pulsate {
            0% { text-shadow: 0 0 5px rgba(14, 227, 255, 0.5); }
            100% { text-shadow: 0 0 20px rgba(14, 227, 255, 0.8), 0 0 30px rgba(14, 227, 255, 0.3); }
        }
        
        .logo::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
            border-radius: 3px;
        }
        
        .tagline {
            text-align: center;
            font-size: 1.2rem;
            color: var(--text-color);
            opacity: 0.8;
            margin-bottom: 20px;
        }
        
        .header-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
        }
        
        .website-info {
            display: flex;
            flex-direction: column;
        }
        
        .website-info .domain {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
            margin-bottom: 5px;
        }
        
        .website-info .date {
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        .overall-score {
            position: relative;
            width: 150px;
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        
        .score-circle {
            position: relative;
            width: 130px;
            height: 130px;
            border-radius: 50%;
            background: conic-gradient(
                var(--primary-color) {{ overall_score }}%, 
                rgba(255, 255, 255, 0.1) {{ overall_score }}%
            );
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 15px rgba(14, 227, 255, 0.3);
            transform-style: preserve-3d;
            perspective: 1000px;
            animation: rotateIn 1s ease-out forwards;
        }
        
        @keyframes rotateIn {
            0% { transform: rotateY(90deg); opacity: 0; }
            100% { transform: rotateY(0); opacity: 1; }
        }
        
        .score-circle::before {
            content: '';
            position: absolute;
            width: 110px;
            height: 110px;
            border-radius: 50%;
            background-color: var(--card-bg);
            z-index: 1;
        }
        
        .score-value {
            position: relative;
            z-index: 2;
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
        }
        
        .score-label {
            position: relative;
            z-index: 2;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        main {
            padding-bottom: 60px;
        }
        
        .analysis-intro {
            text-align: center;
            margin-bottom: 50px;
            padding: 0 20px;
        }
        
        .analysis-intro h2 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            margin-bottom: 15px;
            color: white;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
        }
        
        .analysis-intro p {
            max-width: 800px;
            margin: 0 auto;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .page-cards {
            display: flex;
            flex-direction: column;
            gap: 40px;
        }
        
        .page-card {
            background-color: var(--card-bg);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
            opacity: 0;
            transform: translateY(50px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
        
        .page-card.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        .page-header {
            background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
            padding: 20px;
            position: relative;
            overflow: hidden;
        }
        
        .page-header::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                          rgba(255, 255, 255, 0.1), 
                          rgba(255, 255, 255, 0));
            transform: skewX(-45deg) translateX(-150%);
            animation: sparkle 3s infinite;
        }
        
        @keyframes sparkle {
            0% { transform: skewX(-45deg) translateX(-150%); }
            50% { transform: skewX(-45deg) translateX(150%); }
            100% { transform: skewX(-45deg) translateX(150%); }
        }
        
        .page-title-wrapper {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .page-title {
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 1.3rem;
            color: white;
            margin: 0;
            max-width: 80%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .page-score {
            background-color: rgba(10, 10, 26, 0.8);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 1.2rem;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 10px rgba(14, 227, 255, 0.3);
        }
        
        .page-content {
            padding: 25px;
        }
        
        .data-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .data-item {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid var(--primary-color);
        }
        
        .data-label {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            color: var(--primary-color);
        }
        
        .data-value {
            font-size: 1rem;
        }
        
        .recommendations-section h3 {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            margin-bottom: 20px;
            position: relative;
            display: inline-block;
            color: white;
        }
        
        .recommendations-section h3::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--primary-color), transparent);
        }
        
        .recommendations {
            background-color: rgba(255, 255, 255, 0.03);
            padding: 20px;
            border-radius: 8px;
            white-space: pre-line;
            line-height: 1.7;
        }
        
        .recommendations h2,
        .recommendations h3,
        .recommendations h4 {
            color: white;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        
        .recommendations ul {
            padding-left: 20px;
            margin-bottom: 15px;
        }

        .recommendations strong {
            color: white;
            font-weight: 700;
        }
        
        footer {
            text-align: center;
            padding: 30px 0;
            margin-top: 60px;
            background-color: var(--card-bg);
            position: relative;
            overflow: hidden;
        }
        
        footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
        }
        
        .footer-content {
            position: relative;
            z-index: 1;
        }
        
        .footer-logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 10px;
        }
        
        .footer-text {
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        /* Scroll animation observer for each card */
        @media (prefers-reduced-motion: no-preference) {
            .page-cards .page-card {
                opacity: 0;
                transform: translateY(50px);
                transition: opacity 0.5s ease, transform 0.5s ease;
            }
            
            .page-cards .page-card.visible {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">SEOlyzer</div>
            <div class="tagline">Advanced SEO Analysis & Optimization</div>
            
            <div class="header-info">
                <div class="website-info">
                    <div class="domain">{{ website }}</div>
                    <div class="date">Analyzed on {{ date }}</div>
                </div>
                
                <div class="overall-score">
                    <div class="score-circle">
                        <div class="score-value">{{ overall_score }}</div>
                        <div class="score-label">Score</div>
                    </div>
                </div>
            </div>
        </div>
    </header>
    
    <main class="container">
        <div class="analysis-intro">
            <h2>Website Analysis</h2>
            <p>This report contains a comprehensive SEO audit of {{ website }}. We've analyzed {{ pages|length }} pages, identifying key issues and opportunities for improvement.</p>
        </div>
        
        <div class="page-cards">
            {% for page in pages %}
            <div class="page-card">
                <div class="page-header">
                    <div class="page-title-wrapper">
                        <h2 class="page-title">{{ page.url }}</h2>
                        <div class="page-score">{{ page.score }}</div>
                    </div>
                </div>
                
                <div class="page-content">
                    <div class="data-grid">
                        <div class="data-item">
                            <div class="data-label">Meta Title</div>
                            <div class="data-value">{{ page.meta_title }}</div>
                        </div>
                        
                        <div class="data-item">
                            <div class="data-label">Meta Description</div>
                            <div class="data-value">{{ page.meta_description }}</div>
                        </div>
                        
                        <div class="data-item">
                            <div class="data-label">H1 Tags ({{ page.h1_tags.count }})</div>
                            <div class="data-value">{{ page.h1_tags.contents|join(', ') }}</div>
                        </div>
                        
                        <div class="data-item">
                            <div class="data-label">Word Count</div>
                            <div class="data-value">{{ page.word_count }}</div>
                        </div>
                        
                        <div class="data-item">
                            <div class="data-label">Structured Data</div>
                            <div class="data-value">{{ page.structured_data|join(', ') }}</div>
                        </div>
                    </div>
                    
                    <div class="recommendations-section">
                        <h3>Recommendations</h3>
                        <div class="recommendations">
                            {{ page.recommendations_html|safe }}
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">SEOlyzer</div>
                <div class="footer-text">
                    Advanced SEO Analysis Tool - Report Generated on {{ date }}
                </div>
            </div>
        </div>
    </footer>
    
    <script>
        // Intersection Observer for scroll animations
        document.addEventListener("DOMContentLoaded", function() {
            const cards = document.querySelectorAll('.page-card');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        // Once the animation is complete, unobserve it
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1
            });
            
            cards.forEach(card => {
                observer.observe(card);
            });
            
            // Adjust progress bar gradient for score circles
            const scoreCircle = document.querySelector('.score-circle');
            const score = {{ overall_score }};
            scoreCircle.style.background = `conic-gradient(
                var(--primary-color) ${score}%, 
                rgba(255, 255, 255, 0.1) ${score}%
            )`;
            
            // Set color based on score
            const scoreValue = document.querySelector('.score-value');
            if (score < 40) {
                scoreValue.style.color = '#ff4d4d';
            } else if (score < 70) {
                scoreValue.style.color = '#ffaa00';
            } else {
                scoreValue.style.color = '#00ff9d';
            }
            
            // Set individual page score colors
            const pageScores = document.querySelectorAll('.page-score');
            pageScores.forEach(el => {
                const pageScore = parseInt(el.textContent);
                if (pageScore < 40) {
                    el.style.color = '#ff4d4d';
                } else if (pageScore < 70) {
                    el.style.color = '#ffaa00';
                } else {
                    el.style.color = '#00ff9d';
                }
            });
        });
    </script>
</body>
</html>""")

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(template_dir))

# Load the existing SEO results from file
try:
    with open("seo_results_with_recommendations.json", "r") as f:
        seo_results = json.load(f)
except FileNotFoundError:
    try:
        # Try the other potential filename
        with open("seo_analysis_results.json", "r") as f:
            seo_results = json.load(f)
    except FileNotFoundError:
        print("Error: No SEO results file found. Please run the SEO analysis first.")
        exit(1)

# Prepare the data for the template
context = {
    "title": "SEOlyzer Audit Report",
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "website": next(iter(seo_results)).split('/')[2],  # Extract domain from first URL
    "pages": []
}

# Calculate overall score
overall_score = 0
score_count = 0

# Process each page
for url, data in seo_results.items():
    # Extract recommendations based on data structure
    if "recommendations" in data:  # Format from seo_results_with_recommendations.json
        recommendations = data.get("recommendations", "")
        seo_data = data.get("seo_data", data)  # Use seo_data if available, otherwise use data directly
    else:  # Format from seo_analysis_results.json
        recommendations = "Error generating recommendations"
        seo_data = data
    
    # Extract score from recommendations text
    score = extract_score_from_recommendations(recommendations)
    
    # If score found, add to overall score calculation
    if score > 0:
        overall_score += score
        score_count += 1
    
    # Format recommendations with HTML bold tags
    recommendations_html = format_markdown_to_html(recommendations)
    
    page_data = {
        "url": url,
        "meta_title": seo_data.get("meta_title", "No title"),
        "meta_description": seo_data.get("meta_description", "No description"),
        "h1_tags": seo_data.get("h1_tags", {"count": 0, "contents": ["No H1 tag"]}),
        "word_count": seo_data.get("word_count", 0),
        "structured_data": seo_data.get("structured_data", {}).get("summary", ["No data"]),
        "recommendations": recommendations if isinstance(recommendations, str) else "Error generating recommendations",
        "recommendations_html": recommendations_html if isinstance(recommendations_html, str) else "Error generating recommendations",
        "score": score
    }
    context["pages"].append(page_data)

# Calculate average score
if score_count > 0:
    context["overall_score"] = round(overall_score / score_count)
else:
    context["overall_score"] = 40  # Default score if none found

# Get the template
template = env.get_template("futuristic_template.html")

# Render the template
output = template.render(**context)

# Write to file
output_path = "seolyzer_report.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Styled report generated successfully: {output_path}")
print("Open this file in your browser to view the updated SEOlyzer report.")