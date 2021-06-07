# grpc-chat

## Description

P2P chat implementation on python using grpc technology. One side acts as server and other as client. Client sends messages to the server through simple RPC and server sends messages to the client through response-streaming RPC. If the application runs as a server, the user must provide his own IP address and port. Otherwise, the IP and port of a host should be specified and server should be already running.

Application looks like MVC-architecture application, but there is no model since not much data to operate within P2P chat. Here Server and Client act as Controllers and corresponding GUI classes act as Views.


## Install libraries from [here](https://grpc.io/docs/languages/python/quickstart/#grpc)

## Build proto-based python modules
```python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. chat.proto```
## Run
```python chat.py```
