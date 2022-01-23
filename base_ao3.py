# imports
from bs4 import BeautifulSoup
import time
import requests
import sys
from unidecode import unidecode
import pandas as pd, numpy as np


# class and start_pages
class AO3Page:
    def __init__(self, username, oneshot_only, start_page,
                 include_kudos, include_bookmarks):
        self.username = username
        self.oneshot_only = oneshot_only
        self.start_page = start_page
        self.include_kudos = False
        self.include_bookmarks = False
        self.url = f'https://archiveofourown.org/users/{self.username}/{self.start_page}'
        self.page = 1
        self.all_ids = []
        self.page_empty = False
        self.meta_dict = {}

    def get_ids(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "lxml")
        if self.start_page == 'bookmarks':
            fics = soup.select("li.bookmark.blurb.group")
        elif self.start_page == 'works':
            fics = soup.select("li.work.blurb.group")
        # TODO: other start_pages here
        else:
            sys.exit("Input a valid start page to get work ids!")

        # see if we've gone too far and run out of fic:
        if len(fics) == 0:
            self.page_empty = True
            print("No more fics to fetch!")
            return

        # process list for new fic ids
        for f in fics:
            try:
                i = f.find('h4', class_='heading').find(href=True)['href'].split('/')[-1]
            except:
                continue
            # add work id to list of all ids
            if i not in self.all_ids:
                self.all_ids.append(i)
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

    @staticmethod
    def get_authors(meta):
        tags = meta.contents
        authors = []
        for tag in tags:
            if tag.name == 'a':
                authors.append(tag.contents[0])
        return authors

    @staticmethod
    def get_tag_info(category, meta):
        '''
        given a category and a 'work meta group, returns a list of tags (eg, 'rating' -> 'explicit')
        '''
        try:
            tag_list = meta.find("dd", class_=str(category) + ' tags').find_all(class_="tag")
        except AttributeError as e:
            return []
        return [unidecode(result.text).rstrip().lstrip().lower() for result in tag_list]

    def get_tags(self, meta):
        """
        returns a list of lists
        of rating, category, fandom, pairing, characters, additional_tags
        """
        tags = ['rating', 'category', 'fandom', 'relationship', 'character', 'freeform']
        info_list = list(map(lambda t: self.get_tag_info(t, meta), tags))
        res = {}
        for tag, info in zip(tags, info_list):
            res[tag] = info
        return res

    @staticmethod
    def get_stats(meta):
        categories = ['language', 'published', 'status', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits']
        stats = list(map(lambda category: meta.find("dd", class_=category), categories))
        res = {}
        for cat, stat in zip(categories, stats):
            if stat:
                res[cat] = unidecode(stat.text).rstrip().lstrip().lower()
            else:
                res[cat] = np.nan
        return res

    @staticmethod
    def get_kudos(meta):
        if meta:
            users = []
            # hunt for kudos' contents
            kudos = meta.contents

            # extract user names
            for kudo in kudos:
                if kudo.name == 'a':
                    if 'more users' not in kudo.contents[0] and '(collapse)' not in kudo.contents[0]:
                        users.append(kudo.contents[0])
            return users
        return []

    # get users form bookmarks, excluding yourself
    def get_other_users(self, meta):
        users = []
        for tag in meta:
            user = tag.findChildren("a", recursive=False)[0].contents[0]
            users.append(user)
        return [u for u in users if u != self.username]

    # get bookmarks by page
    def get_bookmarks(self, url):
        bookmarks = []

        req = requests.get(url)
        src = req.text

        time.sleep(5)
        soup = BeautifulSoup(src, 'html.parser')

        # find all pages
        if soup.find('ol', class_='pagination actions'):
            pages = soup.find('ol', class_='pagination actions').findChildren("li", recursive=False)
            max_pages = int(pages[-2].contents[0].contents[0])
            count = 1

            while count <= max_pages:
                # extract each bookmark per user
                tags = soup.findAll('h5', class_='byline heading')
                bookmarks += self.get_other_users(tags)

                # next page
                count += 1
                req = requests.get(url + '?page=' + str(count))
                src = req.text
                soup = BeautifulSoup(src, 'html.parser')
                time.sleep(5)
        else:
            tags = soup.findAll('h5', class_='byline heading')
            bookmarks += self.get_other_users(tags)
        return bookmarks

    @staticmethod
    def access_denied(soup):
        if soup.find(class_="flash error"):
            return True
        if not soup.find(class_="work meta group"):
            return True
        return False

    def get_metadata_from_id(self, fic_id):
        print(f"Scraping {fic_id}...")
        url = f'http://archiveofourown.org/works/{fic_id}?view_adult=true'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        if self.access_denied(soup):
            print('Access Denied')
            time.sleep(10)
            return
        else:
            meta = soup.find("dl", class_="work meta group")
            self.meta_dict["url"] = url

            authors = self.get_authors(soup.find("h3", class_="byline heading"))
            # author column - string if one author
            if len(authors) == 1:
                self.meta_dict["author"] = authors[0]
            else:
                self.meta_dict["author"] = authors

            # unpack tags and stats sub-tags
            for key, value in {**self.get_tags(meta), **self.get_stats(meta)}.items():
                if isinstance(value, list) and len(value) == 1:
                    self.meta_dict[key] = value[0]
                else:
                    self.meta_dict[key] = value

            self.meta_dict["title"] = unidecode(soup.find("h2", class_="title heading").string).strip()

            if self.include_kudos:
                visible_kudos = self.get_kudos(soup.find('p', class_='kudos'))
                hidden_kudos = self.get_kudos(soup.find('span', class_='kudos_expanded hidden'))
                self.meta_dict["all_kudos"] = visible_kudos + hidden_kudos
            if self.include_bookmarks:
                # get bookmarks
                bookmark_url = f'http://archiveofourown.org/works/{fic_id}/bookmarks'
                self.meta_dict["all_bookmarks"] = self.get_bookmarks(bookmark_url)

            return self.meta_dict
