import json
from os import path

import streamlit as st
import pandas as pd
import numpy as np

from src.bookmarks_stats import load_metadata
from src.base_ao3 import AO3Page, flatten_list, update_meta_dict


@st.cache(suppress_st_warning=True)
def get_works(username, authors, oneshot_only):
    # Scrape main user's bookmarks
    file_path = f"data/{username}_authors_metadata.txt"
    if path.exists(file_path):
        with open(file_path) as f:
            meta_dict = json.load(f)
    else:
        meta_dict = {}
        for author in authors:
            st.info(f"Browsing {author}'s works...")
            page = AO3Page(author, oneshot_only, 'works', stats_only=True)
            meta_dict = update_meta_dict(page, meta_dict)
        # write to json
        print("Writing metadata to file...")
        with open(file_path, 'w') as f:
            json.dump(meta_dict, f)
    return meta_dict

def get_all_fics(username, oneshot_only):
    # Scrape user's bookmarked fics
    with st.spinner("Please wait..."):
        meta_dict = load_metadata(username, oneshot_only, False, False)
    meta_df = pd.DataFrame(meta_dict)

    if len(meta_df) == 0:
        st.error("Please enter a valid AO3 username and make sure your bookmarks are public!")
    else:
        # oneshot filter
        if oneshot_only:
            meta_df = meta_df[meta_df['chapters'] == '1/1']

        authors = np.unique(flatten_list(list(meta_df.author)))
        authors_meta_dict = get_works(username, authors, oneshot_only)
        authors_meta_df = pd.DataFrame(authors_meta_dict)

        # find top-rated fics to recommend
        authors_meta_df['year'] = pd.to_datetime(authors_meta_df['published']).dt.year
        authors_meta_df['chaps'] = authors_meta_df['chapters'].str.split('/').str[0]
        for c, w in zip(['comments', 'kudos', 'bookmarks', 'hits'], [1.5, .5, 1, 0.1]):
            authors_meta_df[c] = authors_meta_df[c].astype(float)
            authors_meta_df[f'avg_{c}'] = authors_meta_df[c] / authors_meta_df['chaps'].astype(float)
            authors_meta_df[f'weighted_{c}'] = authors_meta_df[f'avg_{c}'] * w
        authors_meta_df['score'] = authors_meta_df[['weighted_comments', 'weighted_kudos', 'weighted_bookmarks',
                                                    'weighted_hits']].mean(axis=1) / (2022.1 - authors_meta_df['year'])
        read_cond = authors_meta_df['title'].isin(meta_df['title'])
        authors_meta_df = authors_meta_df[~read_cond]
        return authors_meta_df[['title', 'url', 'score']]
