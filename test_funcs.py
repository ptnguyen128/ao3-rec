from bs4 import BeautifulSoup
import re
import time
import requests
import csv
import sys
import datetime
import argparse

page_empty = False
base_url = ""
url = ""
num_requested_fic = 0
num_recorded_fic = 0
csv_name = ""
multichap_only = ""
tags = []

# keep track of all processed ids to avoid repeats:
# this is separate from the temporary batch of ids
# that are written to the csv and then forgotten
seen_ids = []


def get_args():
    """
    Find the correct bookmark URL given a username.
    Initialize other global variables as needed.
    """
    global url
    global csv_name
    global multichap_only

    parser = argparse.ArgumentParser(description='Scrape bookmarked AO3 work IDs given an username')
    parser.add_argument(
        '--username', default='',
        help='your AO3 username')
    parser.add_argument(
        '--out_csv', default='work_ids',
        help='csv output file name')
    parser.add_argument(
        '--multichapter_only', default='no', choices=['yes', 'no'],
        help='yes/no: only retrieve ids for multichapter fics')

    args = parser.parse_args()
    url = f'https://archiveofourown.org/users/{args.username}/bookmarks'
    csv_name = str(args.out_csv)

    multichap_only = str(args.multichapter_only)
    if multichap_only == "yes":
        multichap_only = True
    elif multichap_only == "no":
        multichap_only = False

    return


def get_ids():
    """ Get work ids of bookmarked fics """
    global page_empty
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")

    works = soup.select("li.bookmark.blurb.group")
    # see if we've gone too far and run out of fic:
    if len(works) == 0:
        page_empty = True

    # process list for new fic ids
    ids = []
    for tag in works:
        t = tag.get('id')
        t = t.split('_')[1]
        if t not in seen_ids:
            ids.append(t)
            seen_ids.append(t)
    return ids

# def main():
#     get_args()
#     ids = get_ids()
#     print(ids)

# main()