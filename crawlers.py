import sys
import os
import boto3
from dotenv import dotenv_values

from src.helpers import _s3_file_exists

import streamlit as st
from scrapy.crawler import CrawlerProcess
from scrapeao3.scrapeao3.spiders.bookmarks import BookmarkScraper


def bookmarks_crawler(username):
    """
    Given a username, scrape user's bookmark page
    and write a json file to output
    """
    if os.path.exists('.env'):
        config = dotenv_values(".env")
        for k, v in config.items():
            os.environ[k] = v

    with st.spinner("Just a little bit..."):
        # check if file already existed on S3
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                 aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        bucket = os.environ['S3_BUCKET_NAME']
        file_key = f'bookmarks/{username}.txt'
        if not _s3_file_exists(s3_client, bucket, file_key):
            process = CrawlerProcess(settings={
                "FEED_URI": f's3://streamlit-ao3-data/bookmarks/{username}.txt',
                "FEED_FORMAT": 'json',
                "AWS_ACCESS_KEY_ID": os.environ['AWS_ACCESS_KEY_ID'],
                "AWS_SECRET_ACCESS_KEY": os.environ['AWS_SECRET_ACCESS_KEY'],
                }
            )
            process.crawl(BookmarkScraper,
                          start_urls=[f'https://archiveofourown.org/users/{username}/bookmarks'])
            process.start()
        else:
            print("File already existed.")


if __name__ == '__main__':
    bookmarks_crawler(sys.argv[1])
