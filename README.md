"# grpc-chat" 

python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. chat.proto