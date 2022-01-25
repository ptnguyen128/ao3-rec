from scrapy.item import Item, Field
from itemloaders.processors import MapCompose

def get_work_id(text):
    # check if string includes 'works'
    if 'works' in text:
        # only get id (last element after split)
        return text.split('/')[-1]

def get_work_url(text):
    # check if string includes 'works'
    if 'works' in text:
        # only get id (last element after split)
        return f'https://archiveofourown.com{text}?view_adult=true'

def get_author_url(text):
    # check if not a gift
    if 'gift' not in text:
        # get the whole url
        return f'https://archiveofourown.com{text}/works'

def lower_case(text):
    return text.lower()

def strip_blanks(text):
    return text.rstrip().lstrip()

class WorkItem(Item):
    work_id = Field(
        input_processor=MapCompose(get_work_id)
    )
    work_url = Field(
        input_processor=MapCompose(get_work_url)
    )
    title = Field()
    author = Field()
    author_url = Field(
        input_processor=MapCompose(get_author_url)
    )
    language = Field(
        input_processor=MapCompose(strip_blanks)
    )
    published = Field()
    words = Field()
    fandom = Field()
    rating = Field()
    category = Field()
    pairings = Field(
        input_processor=MapCompose(lower_case)
    )
    tags = Field(
        input_processor=MapCompose(lower_case)
    )
    chapters = Field()
    comments = Field()
    kudos = Field()
    bookmarks = Field()
    hits = Field()
    summary = Field()

