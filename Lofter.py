from bs4 import BeautifulSoup

import urllib
import urllib.request
import re
import os
import sys

class Lofter():
    def __init__(self, url,decode='utf-8'):
        self.url = url
        self.decode = decode
        self.rooturl = 'http://www.lofter.com'

    def get_single_page(url, decode='utf-8'):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        response = urllib.request.Request(url=url, headers=headers)
        html = urllib.request.urlopen(response, timeout=20).read().decode(decode, errors='ignore')
        return html

    def get_pages(url, start_page=1, end_page=None):
        all_pages = []

        if end_page == None:
            pages = None
            while pages != []:
                pages = []
                print('TTT:',url)
                page_url = url + str(start_page)
                html = self.get_single_page(page_url)
                soup = BeautifulSoup(html, "html.parser")
                pages = re.compile(r'"(http://.*.lofter.com/post/.*?)"').findall(str(soup))
                all_pages = all_pages + pages
                start_page += 1
        else:
            for page in range(start_page, end_page + 1):
                pages = []
                page_url = url + str(page)
                print(page_url)
                html = self.get_single_page(page_url)
                soup = BeautifulSoup(html, "html.parser")
                pages = re.compile(r'"(http://.*.lofter.com/post/.*?)"').findall(str(soup))
                all_pages = all_pages + pages
        all_pages = list(set(all_pages))
        return all_pages
