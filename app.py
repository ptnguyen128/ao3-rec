import json
from os import path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

from base_ao3 import AO3Page


@st.cache
def load_metadata(username, oneshot_only, include_kudos, include_bookmarks):
    # Scrape main user's bookmarks
    file_path = f"data/{username}_bookmarks_metadata.txt"
    if path.exists(file_path):
        with open(file_path) as f:
            meta_dict = json.load(f)
    else:
        meta_dict = {}
        page = AO3Page(username, oneshot_only, 'bookmarks', include_kudos, include_bookmarks)
        ids = page.retrieve_ids()
        for fic_id in ids:
            try:
                for key, value in page.get_metadata_from_id(fic_id).items():
                    if key in meta_dict:
                        meta_dict[key].extend([value])
                    else:
                        meta_dict[key] = [value]
            except:
                continue
        # write to json
        print("Writing metadata to file...")
        with open(file_path, 'w') as f:
            json.dump(meta_dict, f)
    return meta_dict


def most_common(lst):
    return max(set(lst), key=lst.count)


def flatten_list(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten_list(el))
        else:
            result.append(el)
    return result


def main():
    # vars
    oneshot_only = False
    include_kudos = False
    include_bookmarks = False

    # Main setup
    st.title('AO3 Fanfic Recommender')
    st.caption("""
    This app takes in your AO3 bookmarks and recommends other fanfics that you might enjoy! (Hopefully) \n
    Created by [@ausoIeil](https://twitter.com/ausoIeil). Still under development.
    """)
    st.markdown("""
    Please enter a valid AO3 username.
    Make sure your bookmarks are public.
    """)
    ## main input - username
    username = st.text_input('AO3 username', value="")

    ## sidebar features
    st.sidebar.header('User Input Features')
    # TODO: add these later
    # extras_options = ['oneshot only', 'include kudos', 'include bookmarks']
    extras_options = ['oneshot only']
    extras = st.sidebar.multiselect("Options", extras_options)
    if 'oneshot only' in extras:
        oneshot_only = True
    if 'include kudos' in extras:
        include_kudos = True
    if 'include bookmarks' in extras:
        include_bookmarks = True

    # Scrape user's bookmarked fics
    with st.spinner("Please wait..."):
        meta_dict = load_metadata(username, oneshot_only, include_kudos, include_bookmarks)
    meta_df = pd.DataFrame(meta_dict)
    if len(meta_df) == 0:
        st.error("Please enter a valid AO3 username!")
    else:
        authors_cnt = len(np.unique(flatten_list(list(meta_df.author))))
        max_lang = most_common(list(meta_df.language))
        max_rating = most_common(flatten_list(list(meta_df.rating)))
        max_fandom = most_common(flatten_list(list(meta_df.fandom)))
        max_pair = most_common(flatten_list(list(meta_df.relationship)))
        max_tag = most_common(flatten_list(list(meta_df.freeform)))

        # write to console
        st.subheader("General Stats")
        st.write(f"""
        You've bookmarked {len(meta_df)} fics by {authors_cnt} authors, 
        mostly rated {max_rating.capitalize()} and in {max_lang.capitalize()}. \n
        """)
        top_choice = st.selectbox("Your favorite", ['fandom', 'relationship', 'tag'])
        if top_choice == 'tag':
            top_var = 'freeform'
        else:
            top_var = top_choice
        count_dict = Counter(flatten_list(list(meta_df[top_var])))
        cnt_df = pd.DataFrame(count_dict.items(), columns=[top_var, 'count'])
        cnt_df = cnt_df.sort_values(['count'], ascending=False).head(10)
        fig = px.pie(cnt_df, top_var, 'count')
        st.plotly_chart(fig)

        most_choice = st.selectbox("Among your bookmarks, the one with the most",
                                   ['words', 'kudos', 'bookmarks', 'hits', 'comments'])
        most_row = meta_df[meta_df[most_choice] == max(meta_df[most_choice])]
        st.write(f"is [{most_row['title'].item()}]({most_row['url'].item()}) - by {most_row['author'].item()}")


if __name__ == "__main__":
    main()
