import os
import time
from concurrent import futures

import grpc
import robohon_message_pb2
import robohon_message_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--mode', help='manual type or read file', type=str, default='manual')
parser.add_argument('--file_name', help='file name for reading the script', type=str, default=None)
args = parser.parse_args()

f = None
if args.mode == 'read_file':
    f = open(args.file_name, 'rb')

class Servicer(robohon_message_pb2_grpc.RoBoHoNMessageServicer):
    def RequestInfo(self, request, context):
        #Get info to send
        print('Got a request type: ', request.info_type)
        if args.mode == 'manual':
            sentence = GetInfo()
        elif args.mode == 'read_file' and not f.tell() == os.fstat(f.fileno()).st_size:
            sentence = f.readline()
        else:
            sentence = ''
        print('Sentence got: ', sentence)
        return robohon_message_pb2.desktop(sentence=sentence)

def GetInfo():
    #Ask for sentence
    sentence = raw_input('Please enter the sentence: ')
    return sentence

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    robohon_message_pb2_grpc.add_RoBoHoNMessageServicer_to_server(Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
        if not f == None:
            f.close()

if __name__ == '__main__':
    serve()
