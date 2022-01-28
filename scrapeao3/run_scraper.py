from scrapeao3.scrapeao3.spiders.bookmarks import BookmarkScraper
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

_MAX_PAGE = 30

class Scraper(object):
    def __init__(self, username, method):
        settings_file_path = 'scrapeao3.scrapeao3.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

        self.crawl_urls = []
        for page in range(1, _MAX_PAGE):
            self.crawl_urls.append(f'https://archiveofourown.org/users/{username}/bookmarks?page={page}')

        # set settings for scraper
        s = get_project_settings()
        # s = {}

        if method == 's3':
            bucket = os.environ['S3_BUCKET_NAME']
            file_key = f'bookmarks/{username}.txt'
            s["FEED_URI"] = f's3://{bucket}/{file_key}'
            s["FEED_FORMAT"] = 'json',
            s["AWS_ACCESS_KEY_ID"] = os.environ['AWS_ACCESS_KEY_ID'],
            s["AWS_SECRET_ACCESS_KEY"] = os.environ['AWS_SECRET_ACCESS_KEY']
        elif method == 'file':
            file_path = f"data/{username}.txt"
            s["FEEDS"] = {file_path: {"format": "json"}}

        # set up process
        self.process = CrawlerProcess(s)
        # test: self.spider = t.QuotesSpider

    def run_spiders(self):
        self.process.crawl(BookmarkScraper, start_urls=self.crawl_urls)
        self.process.start()
