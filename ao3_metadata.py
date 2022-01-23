# imports
import argparse
import pandas as pd, numpy as np
from base_ao3 import AO3Page


def write_fic_metadata(page, file_path):
    ids = page.retrieve_ids()
    print(ids)
    for idx, fic_id in enumerate(ids):
        if idx == 0:
            df = pd.DataFrame([page.get_metadata_from_id(fic_id)])
        else:
            df = pd.concat([df, pd.DataFrame([page.get_metadata_from_id(fic_id)])],
                           ignore_index=True, sort=False)


def main():
    parser = argparse.ArgumentParser(description='Scrape bookmarked AO3 work IDs given an username')
    parser.add_argument(
        '--username', default='',
        help='your AO3 username')
    parser.add_argument(
        '--oneshot_only', default=False,
        help='only retrieve ids for oneshots (fics with only one chapter)')
    parser.add_argument(
        '--start_page', default='bookmarks', choices=['bookmarks', 'works'],
        help=''
    )
    args = parser.parse_args()
    page = AO3Page(args.username, args.oneshot_only,
                   args.start_page, False, False)
    file_path = f"data/{args.username}_{args.start_page}_metadata.csv"

    # t = page.get_ids()[0]
    # print(t.find('h4', class_='heading').find(href=True)['href'])
    ids = page.retrieve_ids()
    print(len(ids))
    # for idx, fic_id in enumerate(ids):
    #     if idx == 0:
    #         df = pd.DataFrame([page.get_metadata_from_id(fic_id)])
    #     else:
    #         df = pd.concat([df, pd.DataFrame([page.get_metadata_from_id(fic_id)])],
    #                        ignore_index=True, sort=False)


    # df = pd.read_csv(file_path, header=0)
    # authors = np.unique(df['author'])
    # for author in authors[:2]:
    #     print(f"Author {author}")
    #     author_file_path = f"data/{author}_works_metadata.csv"
    #     author_page = AO3Page(author, args.oneshot_only, 'works', args.extras)
    #     write_fic_metadata(author_page, author_file_path)
    # return


if __name__ == "__main__":
    main()
