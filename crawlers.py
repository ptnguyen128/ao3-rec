import sys
import os
import boto3

from scrapeao3.src.helpers import set_aws_creds, _s3_file_exists
from scrapeao3.run_scraper import Scraper

_MAX_PAGE = 30
_debug_option = False


def bookmarks_crawler(username, debug=False):
    """
    Given a username, scrape user's bookmark page
    and write a json file to output
    """
    crawl_urls = []
    for page in range(1, _MAX_PAGE):
        crawl_urls.append(f'https://archiveofourown.org/users/{username}/bookmarks?page={page}')

    if debug:
        if not os.path.exists('data'):
            os.makedirs('data')
        file_path = f"data/{username}.txt"

        if not os.path.exists(file_path):
            scraper = Scraper(username, 'file')
            scraper.run_spiders()
        else:
            print("File already existed.")

    else:
        set_aws_creds()
        # check if file already existed on S3
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                 aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        bucket = os.environ['S3_BUCKET_NAME']
        file_key = f'bookmarks/{username}.txt'
        # if file hasn't been written yet, scrape bookmarks
        if not _s3_file_exists(s3_client, bucket, file_key):
            scraper = Scraper(username, 's3')
            scraper.run_spiders()
        else:
            print("File already existed.")

    return 1


if __name__ == '__main__':
    bookmarks_crawler(sys.argv[1], debug=_debug_option)
