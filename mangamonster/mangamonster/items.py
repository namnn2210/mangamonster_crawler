# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime


class MangaClass(scrapy.Item):
    name = scrapy.Field()
    slug = scrapy.Field()
    thumb = scrapy.Field()
    description = scrapy.Field()
    rate = scrapy.Field()
    original = scrapy.Field()
    featured = scrapy.Field()
    type = scrapy.Field()
    ordinal = scrapy.Field()
    chapters = scrapy.Field()
    published = scrapy.Field()
    finished = scrapy.Field()
    status = scrapy.Field()
    manga_author_ids = scrapy.Field()
    manga_genre_ids = scrapy.Field()
    manga_type_id = scrapy.Field()
    meta_tag_id = scrapy.Field()
    created_by = scrapy.Field()
    updated_by = scrapy.Field()
    deleted_by = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    deleted_at = scrapy.Field()
    total_view = scrapy.Field()
    author = scrapy.Field()
    genre = scrapy.Field()
    official_translation = scrapy.Field()
    rss = scrapy.Field()
    weblink = scrapy.Field()
    local_url = scrapy.Field()
    search_text = scrapy.Field()
    search_field = scrapy.Field()


class MangaChapterClass(scrapy.Item):
    name = scrapy.Field()
    slug = scrapy.Field()
    thumb = scrapy.Field()
    description = scrapy.Field()
    original =scrapy.Field()
    ordinal = scrapy.Field()
    season = scrapy.Field()
    published = scrapy.Field()
    status = scrapy.Field()
    manga_id = scrapy.Field()
    meta_tag_id = scrapy.Field()
    resource_status = scrapy.Field()
    created_by = scrapy.Field()
    updated_by = scrapy.Field()
    deleted_by = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    deleted_at = scrapy.Field()
    total_view = scrapy.Field()
    new_slug = scrapy.Field()
    chapter_source = scrapy.Field()
