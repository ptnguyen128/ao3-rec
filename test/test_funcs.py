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
page = 1
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

    fics = soup.select("li.bookmark.blurb.group")
    # see if we've gone too far and run out of fic:
    if len(fics) == 0:
        page_empty = True
        print("No more fics to fetch!")
        return

    # process list for new fic ids
    ids = []
    for idx, f in enumerate(fics):
        try:
            header = f.find('h4', class_='heading').find(href=True)
            t = header['href'].split('/')[-1]
            n = header.text
            if t not in seen_ids:
                ids.append(t)
                seen_ids.append(t)
        except:
            continue
    return ids


def update_url_to_next_page():
    global url
    global page
    key = "page="
    start = url.find(key)

    # there is already a page indicator in the url
    if start != -1:
        # find where in the url the page indicator starts and ends
        page_start_index = start + len(key)
        page_end_index = url.find("&", page_start_index)
        # if it's in the middle of the url
        if page_end_index != -1:
            page = int(url[page_start_index:page_end_index]) + 1
            url = url[:page_start_index] + str(page) + url[page_end_index:]
        # if it's at the end of the url
        else:
            page = int(url[page_start_index:]) + 1
            url = url[:page_start_index] + str(page)

    # there is no page indicator, so we are on page 1
    else:
        # there are other modifiers
        if url.find("?") != -1:
            url = url + "&page=2"
        # there are no modifiers yet
        else:
            url = url + "?page=2"
        page = 2


def retrieve_ids():
    while not page_empty:
        time.sleep(5)
        print(f"Processing page {page}...")
        ids = get_ids()
        update_url_to_next_page()


def main():
    get_args()
    retrieve_ids()
    print(len(seen_ids))
    print(seen_ids)


main()