# imports
from bs4 import BeautifulSoup
import datetime
import time
import requests
import argparse
from unidecode import unidecode
import pandas as pd, numpy as np

from base_ao3 import AO3Page


def main():
    parser = argparse.ArgumentParser(description='Scrape bookmarked AO3 work IDs given an username')
    parser.add_argument(
        '--username', default='',
        help='your AO3 username')
    parser.add_argument(
        '--oneshot_only', default='no', choices=['yes', 'no'],
        help='yes/no: only retrieve ids for oneshots (fics with only one chapter)')
    parser.add_argument(
        '--method', default='bookmarks',
        help='method to retrieve work ids'
    )
    args = parser.parse_args()
    page = AO3Page(args.username, args.oneshot_only, args.method)
    ids = page.retrieve_ids()
    print(ids)


if __name__ == "__main__":
    main()
