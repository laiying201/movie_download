# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
import sys
import random
import time
import urllib.parse

class GetMovieDownloadLink(object):
    """爬取www.dysfz.cc的电影"""
    def __init__(self):
        super(GetMovieDownloadLink, self).__init__()
        self.index_url = 'http://www.dysfz.cc/'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
        cookie = 'dysfz_session=9e26kdf7uuak2fp5g6neudg155; Hm_lvt_2d94c2adebb097cfd3d01af264b039f2=1531933881; PHPSESSID=7ffnhhe6l678hc189e5aqrn7j1'
        self.headers = {'User-Agent': user_agent, 'Cookie': cookie, 'Host': 'www.dysfz.cc'}
        self.session = requests.Session()

    def get_newest_movie_link(self, page=1):
        """获取最新的资源"""
        self.referer_url = 'http://www.dysfz.cc/'
        for i in range(page):
            newest_page_url = 'http://www.dysfz.cc/%s?o=2' % (i)
            self.headers['Referer'] = self.referer_url
            movie_titles, douban_scores, movie_plots, movie_detail_links = self.get_detail_page(newest_page_url)
            for idx in range(len(movie_titles)):
                if i == 1 and idx == 0:
                    continue
                print(movie_titles[idx])
                print(douban_scores[idx])
                print('剧情简介:')
                print(movie_plots[idx])
                print('\n---------资源列表---------\n')
                self.get_detail_info(movie_detail_links[idx])
                print('\n---------分割线---------\n')

    def get_detail_page(self, url):
        """电影简介页面"""
        request = self.session.get(url, headers=self.headers)
        request.encoding = 'utf-8'
        soup = BeautifulSoup(request.text, "html.parser")
        movie_list_rest = soup.find('ul', class_='movie-list reset')
        movie_list = movie_list_rest.find_all('li')
        self.referer_url = url
        self.headers['Referer'] = self.referer_url
        movie_titles = []
        douban_scores = []
        movie_detail_links = []
        movie_plots = []
        for movie_detail in movie_list:
            movie_title = movie_detail.find('h2').get_text()
            try:
                douban_score = movie_detail.find('span', class_='dbscore').get_text()
            except Exception as e:
                douban_score = 'N/A'
            movie_plot = movie_detail.find('div',class_='txt fr').get_text()
            movie_detail_link = movie_detail.find('h2').a.get('href')
            movie_titles.append(movie_title)
            douban_scores.append(douban_score)
            movie_plots.append(movie_plot)
            movie_detail_links.append(movie_detail_link)
        return movie_titles, douban_scores,movie_plots, movie_detail_links

    def get_detail_info(self, detail_page):
        """电影详情页"""
        request_detail = self.session.get(detail_page, headers=self.headers)
        request_detail.encoding = 'utf-8'
        soup_detail = BeautifulSoup(request_detail.text, "html.parser")
        content = soup_detail.find('div', class_='detail')
        for link in content.find_all('p'):
            try:
                href_info = link.find('a')
                download_url = href_info.get('href')
                download_text = href_info.get_text()
            except:
                continue
            if 'ed2k:' in download_url or 'magnet' in download_url or 'ftp://' in download_url or 'thunder' in download_url:
                print(download_text, '---', download_url)
            elif 'pan.baidu.com' in download_url:
                password = re.findall('密码：([a-z0-9A-Z]{4})', link.get_text())
                print(download_url, '---', password)

    def search_movie_link(self, keyword):
        """搜索电影"""
        if keyword == None:
            self.get_newest_movie_link()
            return
        encoding_words = urllib.parse.quote(keyword, encoding='utf-8')
        search_page = 'http://www.dysfz.cc/key/%s/' % (encoding_words)
        movie_titles, douban_scores, movie_plots, movie_detail_links = self.get_detail_page(search_page)
        for i in range(len(movie_titles)):
            print(movie_titles[i])
            print(douban_scores[i])
            print('剧情简介:')
            print(movie_plots[i])
            print('---------资源列表---------')
            self.get_detail_info(movie_detail_links[i])
            print('\n---------分割线---------\n')

    def choice_mod(self, mode=0, page=1, keyword=None):
        """根据模式获取最新电影，或是搜索电影"""
        if mode == 0:
            self.get_newest_movie_link(page)
        else:
            self.search_movie_link(keyword)

if __name__ == '__main__':
    download = GetMovieDownloadLink()
    download.choice_mod(mode=0,page=1)     # 获取最新电影、电视剧、动漫、综艺
    # 搜索电影、电视剧、动漫、综艺
    # download.choice_mod(mode=1,keyword='复仇者联盟')

