import json
from os import path
import csv

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

from src import helpers as h
from .crawlers import bookmarks_crawler as bc


def get_bookmarks_stats(username, oneshot_only, include_kudos, include_bookmarks):
    # Scrape user's bookmarked fics
    meta_dict = bc(username)
    meta_df = pd.DataFrame(meta_dict)

    if len(meta_df) == 0:
        st.error("Please enter a valid AO3 username and make sure your bookmarks are public!")
    else:
        # oneshot filter
        if oneshot_only:
            meta_df = meta_df[meta_df['chapters'] == '1/1']

        authors_cnt = len(np.unique(h.flatten_list(list(meta_df.author))))
        max_lang = h.most_common(list(meta_df.language))
        max_rating = h.most_common(h.flatten_list(list(meta_df.rating)))

        # write to console
        ## general stats
        st.subheader("General Stats")
        st.write(f"""
                You've bookmarked {len(meta_df)} fics by {authors_cnt} authors, 
                mostly rated {max_rating.capitalize()} and in {max_lang.capitalize()}. \n
                """)

        ## count occurrences and display a pie chart of top 10 each category
        top_choice = st.selectbox("Your favorite", ['fandom', 'pairing', 'tag'])
        if top_choice == 'tag':
            top_var = 'freeform'
        elif top_choice == 'pairing':
            top_var = 'relationship'
        else:
            top_var = top_choice
        count_dict = Counter(h.flatten_list(list(meta_df[top_var])))
        cnt_df = pd.DataFrame(count_dict.items(), columns=[top_var, 'count'])
        cnt_df = cnt_df.sort_values(['count'], ascending=False).head(10)
        fig = px.pie(cnt_df, top_var, 'count')
        st.plotly_chart(fig)

        ##  display fic with the most stats (each category)
        most_choice = st.selectbox("Among your bookmarks, the one with the most",
                                   ['words', 'kudos', 'bookmarks', 'hits', 'comments'])
        most_row = meta_df[meta_df[most_choice] == max(meta_df[most_choice])]
        st.write(f"is [{most_row['title'].item()}]({most_row['url'].item()}) - by {most_row['author'].item()}")
