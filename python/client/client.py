#  ../venv/bin/python3 client.py 

import os
import grpc
import pathlib

from google.protobuf.json_format import MessageToDict

from .pb import recognition_config_pb2 as config_pb
from .pb import fluency_service_pb2 as fluency_pb
from .pb import fluency_service_pb2_grpc as fluency_grpcpb

MAX_MESSAGE_LENGTH = 500*1024*1024

project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))

class FluencyClient:
    stub = None

    def __init__(self, remote):
        options = [
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('gprpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        ]
        if remote.endswith('443'):
            if remote.startswith('fluency-svc.baikal.ai'):
                with open(os.path.join(project_path,'ca.cer'), 'rb') as f:
                    creds = grpc.ssl_channel_credentials(f.read())
            else:
                creds = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(
                remote,
                creds,
                options=options)
        else:
            channel = grpc.insecure_channel(
                remote,
                options=options)

        self.stub = fluency_grpcpb.FluencyServiceStub(channel)
    
    def analyze(self, wav_file, engine="baikal-stt") -> fluency_pb.PredictResponse:
        if engine == "whisper":
            engine = config_pb.Engine.WHISPER
        else:
            engine = config_pb.Engine.BaikalSTT
        wave = pathlib.Path(wav_file).read_bytes()
        request = fluency_pb.PredictRequest(wave=wave, engine=engine)
        ret = self.stub.Predict(request)
        return ret 
    
    
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', dest='host', help='remote server host', 
                        default='fluency-svc.baikal.ai', type=str) # gcp load balancer
    parser.add_argument('-port', dest='port',  help='remote server port',
                        default=443, type=int)
    parser.add_argument('-w', dest='wav_file', help='wav file', 
                        default='../resources/sample.wav', type=str)
    parser.add_argument('-e', dest='engine', help='select STT engine', 
                        default='baikal-stt', type=str, choices=["baikal-stt", "whisper"])
    args = parser.parse_args()
    print(args)

    try:
        client = FluencyClient(f'{args.host}:{args.port}')
        result = client.analyze(args.wav_file, args.engine)
        print(MessageToDict(result))
    except Exception as e:
        print(e)
    