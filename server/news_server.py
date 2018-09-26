#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import sys
from concurrent import futures

import grpc
import robohon_message_pb2
import robohon_message_pb2_grpc

sys.path.append('../parser/')
from art2sen import SplitArticle 
from list_news import NewsInfo

def GetArgs():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--news_num', help='number of the news to choose from', type=int, default=3)
    return parser.parse_args()

class Servicer(robohon_message_pb2_grpc.RoBoHoNMessageServicer):
    def __init__(self):
        self.input_s = None
        self.start = None

        # For news reading
        self.news_type = None
        self.news_item = None

    def RequestInfo(self, request, context):
        #Get info to send
        if self.input_s == None:
            sentence = 'empty'
            if self.start == None and request.info_type == 'Start_News':
                self.start = 'News'
                print('Start receiving!')
            elif self.start == 'News':
                self.NewsReading(request.info_type)
        else:
            sentence = self.input_s
            #Wait for RoBoHoN to send back request "Finish"
            if request.info_type == 'Finish' or sentence == 'End':
                self.input_s = None
            else:
                self.input_s = 'empty'
        return robohon_message_pb2.desktop(sentence=sentence)

    def NewsReading(self, info_type):
        if u'国际' in info_type:
            self.news_type = '國際'
        elif u'政治' in info_type:
            self.news_type = '政治'
        elif u'财经' in info_type:
            self.news_type = '財經'
        elif u'娱乐' in info_type:
            self.news_type = '娛樂'
        elif u'运动' in info_type:
            self.news_type = '運動'
        elif u'社会' in info_type:
            self.news_type = '社會'
        elif u'地方' in info_type:
            self.news_type = '地方'
        elif u'生活' in info_type:
            self.news_type = '生活'
        elif u'健康' in info_type:
            self.news_type = '健康'
        elif u'科技' in info_type:
            self.news_type = '科技'
        elif u'旅游' in info_type:
            self.news_type = '旅遊'
        elif u'随便' in info_type:
            self.news_type = '隨便'
        elif u'一' in info_type or '1' in info_type:
            self.news_item = 0
        elif u'二' in info_type or '2' in info_type:
            self.news_item = 1
        elif u'三' in info_type or '3' in info_type:
            self.news_item = 2
        elif not info_type == 'Sentence':
            self.news_type = 'Error'
            self.news_item = 'Error'

class Server(object):
    def __init__(self, news_num):
        self.servicer = Servicer()

        #News Reading
        self.news_num = news_num
        self.news_types = ['國際', '政治', '財經', '娛樂', '運動', '社會', '地方', '生活', '健康', '科技', '旅遊', '隨便']
        self.state = 'Type' #Type, Title, Abstract, Content
        self.questions = self.AskNewsType()
        self.news_item = None

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        robohon_message_pb2_grpc.add_RoBoHoNMessageServicer_to_server(self.servicer, server)
        server.add_insecure_port('[::]:50051')
        server.start()

        try:
            while True:
                if self.servicer.start == None:
                    continue
                elif self.servicer.start == 'News':
                    self.NewsReading()
        except KeyboardInterrupt:
            server.stop(0)

    def AskNewsType(self):
        #questions = ['我可以幫您找以下幾種新聞']
        #questions += self.news_types
        #questions.append('您比較想聽哪一種呢')
        questions = ['請問您想聽哪一種新聞呢']
        return questions

    def AskNewsTitle(self, news_type):
        questions = ['我找到了幾則您可能會想聽的新聞']
        news_info = NewsInfo()
        self.news = news_info.GetNewsInfo(self.news_num, news_type)
        for i in range(len(self.news)):
            questions.append('第' + str(i+1) + '則')
            questions.append(self.news[i][0])
        questions.append('您比較想聽哪一則呢')
        return questions

    def NewsReading(self):
        if not self.questions == [] and self.servicer.input_s == None:
            if len(self.questions) == 1: #The last sentence
                if self.state == 'Type':
                    self.state = 'Title'
                elif self.state == 'Title':
                    self.state = 'Abstract'
                elif self.state == 'Abstract':
                    self.state = 'Content'
                else:
                    self.state = 'Type'
                    self.servicer.start = None
            self.servicer.input_s = self.questions[0]
            del self.questions[0]
        elif self.questions == [] and self.servicer.input_s == None:
            if self.state == 'Title':
                if not self.servicer.news_type == None and not self.servicer.news_type == 'Error':
                    self.questions = self.AskNewsTitle(self.servicer.news_type)
                    self.servicer.news_type = None
                elif self.servicer.news_type == 'Error':
                    self.questions = ['不好意思我沒聽清楚，可以請您再說一次嗎？']
                    self.servicer.news_type = None
                    self.state = 'Type'
            elif self.state == 'Abstract':
                if not self.servicer.news_item == None and not self.servicer.news_item == 'Error':
                    self.news_item = self.servicer.news_item
                    self.questions = ['好的，讓我來為您唸您想聽的新聞']
                    self.servicer.news_item = None
                elif self.servicer.news_item == 'Error':
                    self.questions = ['不好意思我沒聽清楚，可以請您再說一次嗎？']
                    self.servicer.news_item = None
                    self.state = 'Title'
            elif self.state == 'Content':
                #self.questions.extend(SplitArticle(self.news[self.news_item][2]))
                self.questions.append('我唸完了')
                self.questions.append('End') 
            elif self.state == 'Type':
                self.questions = self.AskNewsType()
                self.news_item = None 

if __name__ == '__main__':
    args = GetArgs()

    server = Server(args.news_num)
    server.serve()
