from flask import Flask, render_template_string
import feedparser
from datetime import datetime
import time

app = Flask(__name__)

# HTML template with some basic styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>RSS News Feed</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .article {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .article h2 {
            margin-top: 0;
            color: #333;
        }
        .article a {
            color: #0066cc;
            text-decoration: none;
        }
        .article a:hover {
            text-decoration: underline;
        }
        .meta {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .summary {
            color: #444;
        }
        .refresh-button {
            background-color: #0066cc;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .refresh-button:hover {
            background-color: #0052a3;
        }
    </style>
</head>
<body>
    <h1>Latest News</h1>
    <button class="refresh-button" onclick="window.location.reload()">Refresh News</button>
    
    {% for article in articles %}
    <div class="article">
        <h2><a href="{{ article.link }}" target="_blank">{{ article.title }}</a></h2>
        <div class="meta">Published: {{ article.published }}</div>
        <div class="summary">{{ article.summary[:300] }}...</div>
    </div>
    {% endfor %}
</body>
</html>
"""

class NewsAggregator:
    def __init__(self, feeds):
        self.feeds = feeds

    def get_articles(self):
        articles = []
        for feed_url in self.feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                articles.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', '#'),
                    'published': entry.get('published', 'No date'),
                    'summary': entry.get('summary', entry.get('description', 'No summary available')),
                })
        return articles

@app.route('/')
def home():
    feeds = [
        "https://news.google.com/rss",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "http://rss.cnn.com/rss/cnn_topstories.rss"
    ]
    
    aggregator = NewsAggregator(feeds)
    articles = aggregator.get_articles()
    return render_template_string(HTML_TEMPLATE, articles=articles)

if __name__ == '__main__':
    app.run(debug=True)