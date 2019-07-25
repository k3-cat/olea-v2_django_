import re

import requests
from bs4 import BeautifulSoup

from europaea.id import generate_pid

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


def get_info(attrs):
    base = attrs.pop('base')
    ext = attrs.pop('ext')
    ver = attrs.pop('ver')
    category = attrs['category']

    attrs['pid'] = generate_pid(base=base,
                                pub_date=attrs.pop('pub_date'),
                                category=category,
                                version=ver)

    if category//10 > 1:
        attrs['title'] = base
        attrs['doc_url'] = None
    else:
        attrs['doc_url'] = base
        attrs['title'] = f'{base} - '
        primary = re.match('^scp-(?:cn-)?([0-9]{3,4})(?:(-j)|(-ex))?$', base)
        if primary:
            # SCP-000 SCP-000-J SCP-000-EX
            # SCP-CN-000 SCP-CN-000-J SCP-CN-000-EX
            page = 1
            if '-j' in base:
                url = 'joke-scps'
            elif '-ex' in base:
                url = 'scp-ex'
            else:
                page = int(primary.group(1))//1000 + 1
                url = 'scp-series'
            url += '-cn' if 'cn-' in base else ''
            url += f'-{page}/' if page != 1 else '/'
        elif re.match('^[0-9]{3,4}-jp(-j)?$', base):
            url = 'scp-international/'
        else:
            url = base
            attrs['title'] = ''
        attrs['title'] += fetch_title(base, url, category == 11)

    if ver > 0:
        attrs['title'] += f' ({ext})' if ext else f' ({ver})'

    return attrs
