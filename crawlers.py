import sys
import os

from scrapy.crawler import CrawlerProcess
from scrapeao3.scrapeao3.spiders.bookmarks import BookmarkScraper

def bookmarks_crawler(username):
    """
    Given a username, scrape user's bookmark page
    and write a json file to output
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    file_path = f"data/{username}_bookmarks.txt"
    process = CrawlerProcess(settings={
        "FEEDS": {
            file_path: {"format": "json"},
        },
    })
    process.crawl(BookmarkScraper,
                  start_urls=[f'https://archiveofourown.org/users/{username}/bookmarks'])
    process.start()


if __name__ == '__main__':
    bookmarks_crawler(sys.argv[1])
