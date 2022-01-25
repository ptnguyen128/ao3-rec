import json
from os import path
import csv

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

from src import helpers as h


def get_bookmarks_stats(username, oneshot_only, include_kudos, include_bookmarks):
    # Scrape user's bookmarked fics
    file_path = f"data/{username}_bookmarks.txt"
    if path.exists(file_path):
        with open(file_path) as f:
            meta_dict = json.load(f)
    else:
        meta_dict = {}
    meta_df = pd.DataFrame(meta_dict)

    if len(meta_df) == 0:
        st.error("Please enter a valid AO3 username and make sure your bookmarks are public!")
    else:
        # transform columns
        for c in meta_df.columns:
            if c not in ['fandom', 'pairings', 'tags']:
                meta_df[c] = meta_df[c].apply(lambda x: ''.join(x))
                if c in ['words', 'comments', 'bookmarks', 'kudos', 'hits']:
                    meta_df[c] = meta_df[c].astype(float)

        # oneshot filter
        if oneshot_only:
            meta_df = meta_df[meta_df['chapters'] == '1/1']

        authors_cnt = len(np.unique(h.flatten_list(list(meta_df.author))))
        max_lang = h.most_common(h.flatten_list(list(meta_df.language)))
        max_rating = h.most_common(h.flatten_list(list(meta_df.rating)))

        # write to console
        ## general stats
        st.subheader("General Stats")
        st.write(f"""
                You've bookmarked {len(meta_df)} fics by {authors_cnt} authors, 
                mostly rated {max_rating} and in {max_lang}. \n
                """)

        ## count occurrences and display a pie chart of top 10 each category
        top_choice = st.selectbox("Your favorite", ['fandom', 'pairings', 'tags'])
        count_dict = Counter(h.flatten_list(list(meta_df[top_choice])))
        cnt_df = pd.DataFrame(count_dict.items(), columns=[top_choice, 'count'])
        cnt_df = cnt_df.sort_values(['count'], ascending=False).head(10)
        fig = px.pie(cnt_df, top_choice, 'count')
        st.plotly_chart(fig)

        ##  display fic with the most stats (each category)
        most_choice = st.selectbox("Among your bookmarks, the one with the most",
                                   ['words', 'kudos', 'bookmarks', 'hits', 'comments'])
        most_row = meta_df[meta_df[most_choice] == max(meta_df[most_choice])]
        st.write(f"is [{most_row['title'].item()}]({most_row['work_url'].item()}) - by {most_row['author'].item()}")
