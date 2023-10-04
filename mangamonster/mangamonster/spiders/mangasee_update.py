import scrapy
import re
import json
from . import base_crawler
from loguru import logger

class MangaseeUpdateSpider(scrapy.Spider):
    name = "mangasee_chapter_update"
    allowed_domains = ["mangasee123.com"]
    start_urls = ["https://mangasee123.com/"]

    def parse(self, response):
        script = base_crawler.extract_script_scrapy(response)
        regex = r'vm.LatestJSON\s=\s.{0,};'
        update_str = re.search(regex, script).group()
        list_update_string = update_str.replace('vm.LatestJSON = ', '').replace(';', '')
        list_update = json.loads(list_update_string)
        for update in list_update:
            chapter_encoded = base_crawler.chapter_encode(update['Chapter'])
            index_name = update['IndexName']
            chapter_url = f'https://mangasee123.com/read-online/{index_name}{chapter_encoded}-page-1.html'
            yield response.follow(url=chapter_url, callback=self.parse_chapter_update)
            
    def parse_chapter_update(self, response):
        chapter_source, chapter_info, index_name = base_crawler.get_chapter_info(response)
        new_chapter = {
            'chapter_source': chapter_source,
            'chapter_info':chapter_info
        }
        data = base_crawler.read_json_file(index_name=index_name)
        if data:
            all_chapter_info = data['all_chapter_info']
            update_flag = True
            for chapter in all_chapter_info:
                if chapter == new_chapter:
                    update_flag = False
            if update_flag:
                all_chapter_info.append(new_chapter)
                data['all_chapter_info'] = all_chapter_info
                base_crawler.write_json_file(index_name=index_name, data=data)
                