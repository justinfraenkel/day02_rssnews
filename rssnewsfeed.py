import feedparser
from datetime import datetime
import time
import json
from pathlib import Path

class NewsAgent:
    def __init__(self, rss_url):
        self.rss_url = rss_url
        self.cache_file = Path("news_cache.json")
        self.seen_articles = self.load_cache()
    
    def load_cache(self):
        """Load previously seen articles from cache"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_cache(self):
        """Save seen articles to cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.seen_articles, f)
    
    def fetch_news(self):
        """Fetch and process news articles"""
        try:
            print(f"Attempting to fetch: {self.rss_url}")
            feed = feedparser.parse(self.rss_url)
            
            # Debug information
            print(f"Feed title: {feed.get('feed', {}).get('title', 'No title found')}")
            print(f"Feed status: {feed.get('status', 'No status available')}")
            print(f"Bozo flag: {feed.bozo}")
            print(f"Number of entries: {len(feed.entries)}")
            
            if not feed.entries:
                print(f"No entries found in feed or error fetching feed")
                return []
            
            new_articles = []
            for entry in feed.entries:
                article_id = entry.get('id', entry.link)
                
                # Skip if we've seen this article before
                if article_id in self.seen_articles:
                    continue
                
                article = {
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', 'No link'),
                    'published': entry.get('published', 'No date'),
                    'summary': entry.get('summary', entry.get('description', 'No summary available')),
                }
                
                new_articles.append(article)
                self.seen_articles[article_id] = {
                    'title': article['title'],
                    'timestamp': datetime.now().isoformat()
                }
            
            self.save_cache()
            return new_articles
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e)}")
            return []

def main():
    # Let's try multiple news feeds to see which ones work
    feeds = [
        "http://feeds.reuters.com/reuters/topNews",
        "http://rss.cnn.com/rss/cnn_topstories.rss",
        "https://news.google.com/rss",
        "http://feeds.bbci.co.uk/news/rss.xml"
    ]
    
    agents = [NewsAgent(feed) for feed in feeds]
    
    print("\nFetching latest news...\n")
    for i, agent in enumerate(agents):
        print(f"\nTrying feed #{i + 1}...")
        new_articles = agent.fetch_news()
        
        if new_articles:
            print(f"\nFound {len(new_articles)} new articles:")
            for article in new_articles:
                print("\n-------------------")
                print(f"Title: {article['title']}")
                print(f"Published: {article['published']}")
                print(f"Link: {article['link']}")
                print("Summary:", article['summary'][:200], "..." if len(article['summary']) > 200 else "")
        else:
            print("No new articles found in this feed")

if __name__ == "__main__":
    main()