import os
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.loader import ItemLoader
from ..items import WorkItem


class BookmarkScraper(scrapy.Spider):
    name = 'bookmarks'

    def parse(self, response):
        headers = response.css("li.bookmark.blurb.group")
        for h in headers:
            loader = ItemLoader(item=WorkItem(), selector=h)
            loader.add_value('title', h.css('h4.heading>a::text').get())
            loader.add_css('author', 'h4.heading>a[rel=author]::text')
            loader.add_css('work_id', 'h4.heading>a::attr(href)')
            loader.add_css('work_url', 'h4.heading>a::attr(href)')
            loader.add_css('author_url', 'h4.heading>a[rel=author]::attr(href)')
            loader.add_css('status', '.iswip>span::text')
            loader.add_value('summary', '.userstuff.summary>p::text')
            work_item = loader.load_item()
            links = h.css('h4.heading>a::attr(href)').extract()
            for link in links:
                if 'works' in link:
                    bookmark_url = f'https://archiveofourown.com{link}?view_adult=true'
                    yield response.follow(bookmark_url, self.parse_work, meta={'work_item': work_item})

        # next_url = response.css("ol.pagination.actions>li.next").get()
        # yield response.follow(next_url, callback=self.parse)

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

