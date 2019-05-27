import requests
from bs4 import BeautifulSoup


CN_SITE_URL = 'http://scp-wiki-cn.wikidot.com'
EN_SITE_URL = 'http://scp-wiki-cn.wikidot.com'


# TODO use real cache
class PageCache:
    page_soup = dict()

    @staticmethod
    def clear_cache():
        PageCache.page_soup.clear()


def fetch_title(url_, url, eng):
    if url not in PageCache.page_soup:
        html = requests.get(f'{CN_SITE_URL if not eng else EN_SITE_URL}/{url}')
        _soup = BeautifulSoup(html.text, 'lxml')
        PageCache.page_soup[url] = _soup.find_all(
            name='div',
            attrs={'class': 'content-panel standalone series'},
            limit=1)[0]
    main_contant = PageCache.page_soup[url]
    try:
        ele_title = main_contant.find_all(name='a', text=url_, limit=1)[0]
    except IndexError:
        raise Exception('cannot find title')
    if not ele_title:
        raise Exception('cannot find title')
    return ele_title.parent.text
