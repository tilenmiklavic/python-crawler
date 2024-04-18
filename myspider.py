import scrapy
import json
from datetime import datetime

class LinkSpider(scrapy.Spider):
    name = 'link_spider'
    allowed_domains = []  # Optional: limit to specific domains
    start_urls = ['https://med.over.net/forum/']  # Start with your initial URL

    def parse(self, response):
        # Extract the title of the page
        title = response.css('title::text').get() or "No title"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract text from all elements with the class 'forum-post__content'
        posts = response.css('.forum-post__content').getall()
        posts = [post.strip() for post in posts]  # Clean whitespace

        # Prepare data to write to JSON
        data = {
            'url': response.url,
            'title': title,
            'timestamp': current_time,
            'posts': posts
        }
        
        # Write data to JSON file
        with open('titles_and_timestamps.json', 'a') as file:
            if len(posts) > 0:
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write('\n')  # Ensure each entry is on a new line
        
        # Log the title and timestamp to the console as well
        self.log(f"Saved {title} with timestamp {current_time} from {response.url}")

        # Find all links within the page's <a> tags and yield new requests
        for href in response.css('a::attr(href)').getall():
            full_url = response.urljoin(href)
            yield scrapy.Request(url=full_url, callback=self.parse)
