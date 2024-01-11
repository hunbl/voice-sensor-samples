#!/bin/bash
PROTO=baikal/speech
PY_LIB=../python/client/pb

python -m grpc_tools.protoc --proto_path=$PROTO:. --python_out=$PY_LIB --grpc_python_out=$PY_LIB $PROTO/fluency_service.proto
python -m grpc_tools.protoc --proto_path=$PROTO --python_out=$PY_LIB --grpc_python_out=$PY_LIB $PROTO/recognition_config.proto
