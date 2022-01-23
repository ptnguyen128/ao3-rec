# imports
from bs4 import BeautifulSoup
import sys
import requests


# class and methods
class AO3Page:
    def __init__(self, username, oneshot_only, method):
        self.username = username
        self.oneshot_only = oneshot_only
        self.method = method
        self.url = f'https://archiveofourown.org/users/{self.username}/bookmarks'
        self.page = 1
        self.all_ids = []
        self.page_empty = False

    def get_ids(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "lxml")
        if self.method == 'bookmarks':
            fics = soup.select("li.bookmark.blurb.group")
        # TODO: other methods here
        else:
            sys.exit("Input a valid method to get work ids!")

        # see if we've gone too far and run out of fic:
        if len(fics) == 0:
            self.page_empty = True
            print("No more fics to fetch!")
            return

        # process list for new fic ids
        for idx, f in enumerate(fics):
            if self.method == 'bookmarks':
                try:
                    header = f.find('h4', class_='heading').find(href=True)
                    t = header['href'].split('/')[-1]
                except TypeError:
                    continue
            # TODO: other methods here
            if t not in self.all_ids:
                self.all_ids.append(t)
        return

    def update_url_to_next_page(self):
        key = "page="
        start = self.url.find(key)

        # there is already a page indicator in the url
        if start != -1:
            # find where in the url the page indicator starts and ends
            page_start_index = start + len(key)
            page_end_index = self.url.find("&", page_start_index)
            # if it's in the middle of the url
            if page_end_index != -1:
                self.page = int(self.url[page_start_index:page_end_index]) + 1
                self.url = self.url[:page_start_index] + str(self.page) + self.url[page_end_index:]
            # if it's at the end of the url
            else:
                self.page = int(self.url[page_start_index:]) + 1
                self.url = self.url[:page_start_index] + str(self.page)

        # there is no page indicator, so we are on page 1
        else:
            # there are other modifiers
            if self.url.find("?") != -1:
                self.url += "&page=2"
            # there are no modifiers yet
            else:
                self.url += "?page=2"
            self.page = 2

    def retrieve_ids(self):
        while not self.page_empty:
            print(f"Processing page {self.page}...")
            self.get_ids()
            self.update_url_to_next_page()
        return self.all_ids

