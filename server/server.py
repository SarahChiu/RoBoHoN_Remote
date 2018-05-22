import os
import time
import sys
from concurrent import futures

import grpc
import robohon_message_pb2
import robohon_message_pb2_grpc

sys.path.append('../parser/')
from art2sen import SplitArticle 

def GetArgs():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mode', help='manual, read_file, or url', type=str, default='manual')
    parser.add_argument('--file_name', help='file name for reading the script', type=str, default='sentences.txt')
    parser.add_argument('--url', help='url of the article to read', type=str, default='http://newtalk.tw/news/view/2018-05-21/125054')
    return parser.parse_args()

class Servicer(robohon_message_pb2_grpc.RoBoHoNMessageServicer):
    def RequestInfo(self, request, context):
        #Get info to send
        global input_s
        if input_s == None:
            sentence = 'empty'
        else:
            sentence = input_s
            #Wait for RoBoHoN to send back request "Finish"
            if request.info_type == "Finish":
                input_s = None
            else:
                input_s = 'empty'
        return robohon_message_pb2.desktop(sentence=sentence)

def GetInfo(args, f=None, sentences=None, sen_num=None):
    #Ask for sentence
    global input_s
    if args.mode == 'manual': 
        if sys.version_info[0] == 2:
            input_s = raw_input('Please enter the sentence: ')
        elif sys.version_info[0] == 3:
            input_s = input('Please enter the sentence: ')
        else:
            raise Exception('Python version error!')
    elif args.mode == 'read_file' and not f.tell() == os.fstat(f.fileno()).st_size:
        if input_s == None:
            time.sleep(0.01)
            input_s = f.readline()
    elif args.mode == 'url' and sen_num < len(sentences) and not sen_num == None:
        if input_s == None:
            time.sleep(0.01)
            input_s = sentences[sen_num]
            sen_num += 1
        return sen_num

def serve():
    args = GetArgs()

    if args.mode == 'read_file':
        f = open(args.file_name, 'rb')
    elif args.mode == 'url':
        sentences = SplitArticle(args.url)
        sen_num = 0

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    robohon_message_pb2_grpc.add_RoBoHoNMessageServicer_to_server(Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            if args.mode == 'manual':
                GetInfo(args)
            elif args.mode == 'read_file':
                GetInfo(args, f=f)
            elif args.mode == 'url':
                sen_num = GetInfo(args, sentences=sentences, sen_num=sen_num)
            else:
                raise Exception('Mode not implemented!')
    except KeyboardInterrupt:
        server.stop(0)
        if args.mode == 'read_file':
            f.close()

if __name__ == '__main__':
    global input_s
    input_s = None

    serve()
