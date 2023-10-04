from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import re
import json

def get_soup(url):
    return BeautifulSoup(urlopen(Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 'Cookie':'PHPSESSID=bh09hfshmt9fhnqkmkg2v3rflj; _ga=GA1.2.459389766.1692582622; _gid=GA1.2.2016220288.1692582622; _ga_5HPMBJPE7W=GS1.2.1692582622.1.0.1692582622.0.0.0'})),
                                     'html.parser')

def extract_script_bs4(url):
    soup = get_soup(url)
    return soup.find_all('script')[-1].text

def extract_script_scrapy(response):
    return response.css('script')[-1].get()

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

def get_chapter_info(response):
    chapter_script = extract_script_scrapy(response)
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

def read_json_file(index_name):
    try:
        with open(f'mangasee_json/{index_name}.json','r') as file:
            data = json.load(file)
        return data
    except Exception as ex:
        return None

def write_json_file(index_name, data):
    with open(f'mangasee_json/{index_name}.json','w') as file:
        json.dump(data, file)