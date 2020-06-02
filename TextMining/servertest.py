from socket import *
import json

print("들어올 데이터를 기다리는 중입니다.")

IP = ''
PORT = 9999

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

with server_socket:
    server_socket.bind((IP, PORT))
    server_socket.listen()  #클라이언트의 요청을 받을 준비

    while True:
        client_socket, client_addr = server_socket.accept()
        print(str(client_addr), '에서 접속이 확인되었습니다.')

        data = client_socket.recv(4)
        # 최초 4바이트는 전송할 데이터의 크기이다. 그 크기는 little big 엔디언으로 byte에서 int형식으로 변환한다.
        length = int.from_bytes(data, "little")
        # 다시 데이터를 수신한다.
        data = client_socket.recv(length)
        # 수신된 데이터를 str형식으로 decode한다.
        msg = data.decode()
        # 수신된 메시지를 콘솔에 출력한다.
        print('받은 데이터 : ', msg)

        fname = r'/home/ubuntu/handypotter/v2t.txt'
        f = open(fname, 'w')
        f.write(msg)
        f.close()

        from textmining import *
        from comparingSL import *
        from synonym import *

        id_list = Synonym.getresult()
        emo = Textmining.emoDictionary(msg)

        returnSL = " ".join(map(str, id_list))
        returnEMO = " ".join(map(str, emo))
        returnvalue = returnSL + "\n" +returnEMO
        returnvalue = returnvalue.encode()
        length = len(returnvalue)
        client_socket.sendall(length.to_bytes(4, byteorder='little'))
        client_socket.sendall(returnvalue)
        print('메시지를 보냈습니다.')
