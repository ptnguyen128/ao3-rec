import sys
import os
import boto3

from src.helpers import _s3_file_exists
from _creds import aws_creds

import streamlit as st
from scrapy.crawler import CrawlerProcess
from scrapeao3.scrapeao3.spiders.bookmarks import BookmarkScraper


def bookmarks_crawler(username):
    """
    Given a username, scrape user's bookmark page
    and write a json file to output
    """
    with st.spinner("Just a little bit..."):
        # check if file already existed on S3
        s3_client = boto3.client('s3',
                                 aws_access_key_id=aws_creds['access_key_id'],
                                 aws_secret_access_key=aws_creds['secret_access_key'])
        bucket = 'streamlit-ao3-data'
        file_key = f'bookmarks/{username}.txt'
        if not _s3_file_exists(s3_client, bucket, file_key):
            process = CrawlerProcess(settings={
                "FEED_URI": f's3://streamlit-ao3-data/bookmarks/{username}.txt',
                "FEED_FORMAT": 'json',
                "AWS_ACCESS_KEY_ID": aws_creds['access_key_id'],
                "AWS_SECRET_ACCESS_KEY": aws_creds['secret_access_key'],
                }
            )
            process.crawl(BookmarkScraper,
                          start_urls=[f'https://archiveofourown.org/users/{username}/bookmarks'])
            process.start()
        else:
            print("File already existed.")


if __name__ == '__main__':
    bookmarks_crawler(sys.argv[1])
