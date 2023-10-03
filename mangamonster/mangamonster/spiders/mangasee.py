import scrapy
import re
import json
from . import base_crawler

def extract_script(response):
    return response.css('script')[-1].get()

def get_list_chapters(response):
    manga_script = extract_script(response)
    regex = r'vm.Chapters\s=\s.{0,};'
    match = re.search(regex, manga_script)
    if match:
        list_chapters_str = match.group()
        a = list_chapters_str.replace('vm.Chapters = ', '').replace(';', '')
        list_chapters = a.strip('][').split('},')
        size_list_chapters = len(list_chapters)
        # logger.info('SIZE LIST CHAPTERS: %s' % size_list_chapters)
        return list_chapters
    else:
        return None
    
def chapter_encode(chapter_string):
    index = ''
    index_string = chapter_string[0:1]
    if index_string != '1':
        index = '-index-{}'.format(index_string)
    chapter = int(chapter_string[1:-1])
    odd = ''
    odd_string = chapter_string[len(chapter_string) - 1]
    if odd_string != '0':
        odd = '.{}'.format(odd_string)
    return '-chapter-{}{}{}'.format(chapter, odd, index)

def get_chapter_info(chapter_url):
    chapter_script = base_crawler.extract_script(chapter_url)
    chapter_regex = r'vm.CurChapter\s=\s.{0,};'
    chapter_source_regex = r'vm.CurPathName\s=\s.{0,};'
    index_name_regex = r'vm.IndexName\s=\s.{0,};'
    source_match = re.search(chapter_source_regex, chapter_script)
    if source_match:
        chapter_source_str = source_match.group()
        chapter_source = chapter_source_str.replace('vm.CurPathName = ', '').replace(';', '').replace('"', '')
    info_match = re.search(chapter_regex, chapter_script)
    if info_match:
        chapter_str = info_match.group()
        chapter_info = json.loads(chapter_str.replace('vm.CurChapter = ', '').replace(';', ''))
    index_match = re.search(index_name_regex, chapter_script)
    if index_match:
        index_name_str = index_match.group()
        index_name = index_name_str.replace('vm.IndexName = ', '').replace(';', '').replace('"', '')
    return chapter_source, chapter_info, index_name


class MangaseeSpider(scrapy.Spider):
    name = "mangasee"
    allowed_domains = ["mangasee123.com"]
    start_urls = ["https://mangasee123.com/search/"]

    def parse(self, response):
        script = extract_script(response)
        regex = r'vm.Directory\s=\s.{0,};'
        manga_str = re.search(regex, script).group()
        list_mangas_string = manga_str.replace('vm.Directory = ', '').replace(';', '')
        list_mangas = json.loads(list_mangas_string)
        for manga in list_mangas:
            index_name = manga['i']
            manga_url = f'https://mangasee123.com/manga/{index_name}'
            yield response.follow(url=manga_url, callback=self.parse_list_mangas, meta={'manga':manga})
    
    def parse_list_mangas(self, response):
        manga = response.meta.get('manga')
        index_name = manga['i']
        list_chapters = get_list_chapters(response)
        manga['chapter_size'] = len(list_chapters)
        manga_chapter_info = []
        for chapter in list_chapters:
            if not chapter.endswith('}'):
                chapter += '}'
            chapter_json = json.loads(chapter)
            chapter_encoded = chapter_encode(chapter_json['Chapter'])
            chapter_url = f'https://mangasee123.com/read-online/{index_name}{chapter_encoded}-page-1.html'
            chapter_source, chapter_info, _ = get_chapter_info(chapter_url)
            manga_chapter_info.append({
                'chapter_source':chapter_source,
                'chapter_info': chapter_info,
            })
        manga['all_chapter_info'] = manga_chapter_info
        with open(f"mangasee_json/{index_name}.json", "w") as file:
            json.dump(manga, file)


        