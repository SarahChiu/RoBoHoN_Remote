#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup

class NewsInfo(object):
    def GetNewsInfo(self, news_num, news_type):
        if news_type == '國際':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/world')
        elif news_type == '政治':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/politics')
        elif news_type == '財經':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/finance')
        elif news_type == '娛樂':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/entertainment')
        elif news_type == '運動':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/sports')
        elif news_type == '社會':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/society')
        elif news_type == '地方':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/local')
        elif news_type == '生活':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/lifestyle')
        elif news_type == '健康':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/health')
        elif news_type == '科技':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/technology')
        elif news_type == '旅遊':
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss/travel')
        else:
            xml_page = urllib.urlopen('https://tw.news.yahoo.com/rss')

        soup = BeautifulSoup(xml_page, 'xml')
        news_info = soup.findAll('item')
        news_num = min(len(news_info), news_num)
        output_news = []
        for n in range(news_num):
            title = str(news_info[n].findAll('title')[0])
            title = title.replace('<title>', '')
            title = title.replace('</title>', '')
            description = str(news_info[n].findAll('description')[0])
            description = description.replace('<description>', '')
            description = description.replace('</description>', '')
            link = str(news_info[n].findAll('link')[0])
            link = link.replace('<link>', '')
            link = link.replace('</link>', '')
            output_news.append([title, description, link])
        return output_news

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--news_num', help='number of news to list', type=int, default=5)
    parser.add_argument('--news_type', help='the type of the news', type=str, default=None)
    args = parser.parse_args()

    news_info = NewsInfo()
    news = news_info.GetNewsInfo(args.news_num, args.news_type)
    for n in news:
        print(n[0])
        print(n[1])
        print(n[2])
