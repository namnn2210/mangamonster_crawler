from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_soup(url):
    return BeautifulSoup(urlopen(Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 'Cookie':'PHPSESSID=bh09hfshmt9fhnqkmkg2v3rflj; _ga=GA1.2.459389766.1692582622; _gid=GA1.2.2016220288.1692582622; _ga_5HPMBJPE7W=GS1.2.1692582622.1.0.1692582622.0.0.0'})),
                                     'html.parser')

def extract_script(url):
    soup = get_soup(url)
    return soup.find_all('script')[-1].text