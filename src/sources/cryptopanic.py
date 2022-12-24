from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs

class Cryptopanic:
    """
    Class for cryptopanic data source management
    """
    def __init__(self, rss_url="https://cryptopanic.com/news/rss/", filters=None):
        # filters will be used in the future, e.g., trending, popular, etc.
        self.rss_url = rss_url
    
    def get_new_rss(self, last_pubdate=None):
        new_posts = []
        soup = bs(requests.get(self.rss_url).content, "xml")
        # RSS feed starts from newest to oldest, so it will need to be 
        # returned .reverse() in order to be posted at the right order.
        for item in soup.find_all("item"):
            if last_pubdate is None:
                new_posts.append([item.pubDate.text, item.title.text, item.link.text])
                continue

            if self.is_date_newer(item.pubDate.text, last_pubdate):
                new_posts.append([item.pubDate.text, item.title.text, item.link.text])
            
            

        new_posts.reverse()
        return new_posts
            
    
    def is_date_newer(self, date: str, date2: str):
        """ 
        Checks if the first date is newer, if yes
        returns True
        e.g. date format = 'Sat, 24 Dec 2022 21:33:21 +0000' 
        """
        directives = "%a, %d %b %Y %H:%M:%S %z"
        first_date = datetime.strptime(date, directives)
        second_date = datetime.strptime(date2, directives)
        return first_date > second_date
