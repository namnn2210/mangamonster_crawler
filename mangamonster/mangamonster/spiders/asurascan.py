import scrapy
from loguru import logger
from datetime import datetime
import re

class AsurascanSpider(scrapy.Spider):
    name = "asurascan"
    allowed_domains = ["asuracomics.com"]
    start_urls = ["https://asuracomics.com/manga/?page=1&order=update"]

    def parse(self, response):
        div_bs = response.css('div.bs')
        for div in div_bs:
            manga_url = div.css('div.bsx a::attr(href)').get()
            yield response.follow(manga_url, callback=self.parse_manga)
            
        div_hpage = response.css('div.hpage a.r')
        if div_hpage:
            next_page_url = div_hpage.attrib.get('href')
            r_link = f'https://asuracomics.com/manga/{next_page_url}'
            # Follow the link to the next page
            yield response.follow(r_link, callback=self.parse)
            
    def parse_manga(self,response):
        manga_url = response.url.split('/')[-2]
        # Use a regular expression to match the desired text portion
        match = re.search(r'-(.*)$', manga_url)
        if match:
            slug = match.group(1)
        else:
            print("No match found.")
        info_box = response.css('div.bigcontent')
        thumb_url = info_box.css('div.thumb img.wp-post-image::attr(src)').get()
        logger.info(thumb_url)
        today = datetime.now()
        today_str = '{}/{}/{}'.format(str(today.year), str(today.month), str(today.day))
        thumb_path = 'images/manga/{}/{}.jpg'.format(today_str, slug)
        thumb_save_path = f'/www-data/mangamonster.com/storage/app/public/{thumb_path}'
        logger.info(thumb_save_path)
        list_chapters = response.css('ul.clstyle li')
        for chapter in list_chapters:
            chapter_url = chapter.css('div.eph-num a::attr(href)').get()
            ordinal = chapter.css('::attr(data-num)').get()
            yield response.follow(chapter_url, callback=self.parse_manga_chapter)
            
            
    def parse_manga_chapter(self,response):
        resource_divs = response.css('div#readerarea p img')
        for resource in resource_divs:
            resource_img = resource.css('::attr(src)').get()
            logger.info(resource_img)
        
