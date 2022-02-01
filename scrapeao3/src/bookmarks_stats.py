import json
import os

import boto3
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

import scrapeao3.src.helpers as h


def get_bookmarks_stats(username, oneshot_only, completed_only,
                        include_kudos, include_bookmarks, debug=False):
    if debug:
        # Scrape user's bookmarked fics
        file_path = f"data/{username}.txt"
        if os.path.exists(file_path):
            with open(file_path) as f:
                meta_dict = json.load(f)
        else:
            meta_dict = {}
        meta_df = pd.DataFrame(meta_dict)
    else:
        # Read bookmark metadata file from S3
        h.set_aws_creds()
        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                     aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        bucket = os.environ['S3_BUCKET_NAME']
        file_key = f'bookmarks/{username}.txt'

        try:
            content_object = s3_resource.Object(bucket, file_key)
            file_content = content_object.get()['Body'].read().decode('utf-8')
            meta_dict = json.loads(file_content)
        except:
            meta_dict = {}
        meta_df = pd.DataFrame(meta_dict)

    if len(meta_df) == 0:
        st.error("Please enter a valid AO3 username and make sure your bookmarks are public!")
    else:
        # transform columns
        for c in meta_df.columns:
            if c in ['title', 'work_id', 'work_url', 'status', 'summary',
                     'language', 'published', 'chapters', 'rating',
                     'words', 'comments', 'bookmarks', 'kudos', 'hits']:
                meta_df[c] = meta_df[c].apply((lambda x: ''.join(x) if pd.notnull(x) else ''))
                if c in ['words', 'comments', 'bookmarks', 'kudos', 'hits']:
                    meta_df[c] = meta_df[c].replace('', 0).astype(float)

        # oneshot filter
        if oneshot_only:
            meta_df = meta_df[meta_df['chapters'] == '1/1']
        # completion filter
        if completed_only:
            meta_df = meta_df[meta_df['status'] == 'Complete Work']

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
