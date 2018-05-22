#!/usr/bin/python
# -*- coding: utf-8 -*-

from goose import Goose
from goose.text import StopWordsChinese

def SplitArticle(url):
    g = Goose({'stopwords_class': StopWordsChinese})
    article = g.extract(url=url)

    total_words = len(article.cleaned_text)
    current_word = 0
    last_sentence = ''
    sentences_pool = []
    while current_word < total_words:
        sub_article = last_sentence + article.cleaned_text[current_word:min(current_word+100, total_words)]
        complete = (sub_article[-1] == u'。')
        sentences = sub_article.split(u'。')
        for s in range(len(sentences)-1):
            for sub_s in sentences[s].split('\n'):
                if not sub_s == '':
                    sentences_pool.append(sub_s.encode('utf-8')+'\n')

        if not complete:
            last_sentence = sentences[-1]
        else:
            last_sentence = ''
            for sub_s in sentences[-1].split('\n'):
                if not sub_s == '':
                    sentences_pool.append(sub_s.encode('utf-8')+'\n')
        
        current_word = min(current_word+100, total_words)

    return sentences_pool

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--url', help='the url of the article', type=str, default='http://www.bbc.co.uk/zhongwen/simp/chinese_news/2012/12/121210_hongkong_politics.shtml')
    parser.add_argument('--out_file', help='file contains the result sentences', type=str, default=None)
    args = parser.parse_args()

    sentences = SplitArticle(args.url)
    if not args.out_file == None:
        f = open(args.out_file, 'wb')
        for s in sentences:
            f.write(s)
        f.close()
