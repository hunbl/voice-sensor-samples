#  venv/bin/python3 sample.py 

import os
import grpc
import pathlib

from google.protobuf.json_format import MessageToDict

from client import FluencyClient

fluency_svc = 'fluency-svc.baikal.ai:443'

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='wav_file', help='wav file', 
                        default='../resources/sample.wav', type=str)
    parser.add_argument('-e', dest='engine', help='select STT engine', 
                        default='baikal-stt', type=str, choices=["baikal-stt", "whisper"])
    args = parser.parse_args()
    print(args)

    try:
        # 서비스 클라이언트 생성
        cli = FluencyClient(fluency_svc)
        # 음성파일을 전송하고 결과를 받는다.
        #   engine = baikal-stt: 속도가 빠르고 음절 분할 정확. 문장이 틀리더라도 들리는 대로 전사하는 경우 사용
        #   engine = whisper: whisper 라지모델을 사용하므로 느리지만 문장 정확도 높아여 하는 경우
        result = cli.analyze(args.wav_file, args.engine)
        print(MessageToDict(result))
    except Exception as e:
        print(e)
