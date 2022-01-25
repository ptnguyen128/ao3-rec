import os
import scrapy
import time
from scrapy.loader import ItemLoader
from ..items import WorkItem


class BookmarkScraper(scrapy.Spider):
    name = 'bookmarks'

    def parse(self, response):
        bookmarks = response.css(".bookmark.blurb.group")
        for b in bookmarks:
            loader = ItemLoader(item=WorkItem(), selector=b)
            loader.add_value('title', b.css('h4.heading>a::text').get())
            loader.add_css('author', 'h4.heading>a[rel=author]::text')
            loader.add_css('work_id', 'h4.heading>a::attr(href)')
            loader.add_css('work_url', 'h4.heading>a::attr(href)')
            loader.add_css('author_url', 'h4.heading>a[rel=author]::attr(href)')
            loader.add_css('summary', '.userstuff.summary>p::text')
            work_item = loader.load_item()
            links = b.css('h4.heading>a::attr(href)').extract()
            for link in links:
                if 'works' in link:
                    bookmark_url = f'https://archiveofourown.com{link}?view_adult=true'
            yield response.follow(bookmark_url, self.parse_work, meta={'work_item': work_item})

        # go to next page
        for a in response.css('li.next a'):
            time.sleep(10)
            yield response.follow(a, self.parse)

    def parse_work(self, response):
        work_item = response.meta['work_item']
        loader = ItemLoader(item=work_item, response=response)
        for stat in ['language', 'published', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits']:
            loader.add_css(stat, f'dd.{stat}>a::text, dd.{stat}::text')
        loader.add_css('fandom', 'h5.fandoms.heading>a::text, dd.fandom.tags>ul>li>a::text')
        loader.add_css('rating', 'span.rating>span::text, dd.rating.tags>ul>li>a::text')
        loader.add_css('category', 'span.category>span::text, dd.category.tags>ul>li>a::text')
        loader.add_css('pairings', 'li.relationships>a.tag::text, dd.relationship.tags>ul>li>a::text')
        loader.add_css('tags', 'li.freeforms>a.tag::text, dd.freeform.tags>ul>li>a::text')
        yield loader.load_item()

