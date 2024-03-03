import socket
import json
import select
import ssl

quiz_data = {
    'questions': [
        {'question': 'What is the capital of France?', 'options': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'},
        # Add more questions as needed
    ]
}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('10.1.20.33', 12345))

server_socket.listen(5)
connected_clients = {}
score_dict = {}

while True:
    readable, _, _ = select.select([server_socket] + list(connected_clients.keys()), [], [])

    for sock in readable:
        if sock is server_socket:
            client_socket, client_address = server_socket.accept()

            ssl_client_socket = ssl.wrap_socket(client_socket, server_side=True, keyfile='server_key.pem', certfile='server_cert.pem', ssl_version=ssl.PROTOCOL_TLS)
            connected_clients[ssl_client_socket] = client_address

            first_question = json.dumps(quiz_data['questions'][0])
            ssl_client_socket.send(first_question.encode())
        else:
            try:
                answer = sock.recv(1024).decode()

                if not answer:
                    address = connected_clients.pop(sock, None)
                    if address:
                        score_dict[address[0]] = score_dict.get(address[0], 0)
                        score_dict[address[0]] += score

                    sock.close()

                    print("Current Scores:")
                    for ip, score in score_dict.items():
                        print(f"{ip}:{score}")

                else:
                    if answer == quiz_data['questions'][0]['answer']:
                        score = 1
                    else:
                        score = 0

                    sock.send(str(score).encode())

            except ConnectionResetError:
                address = connected_clients.pop(sock, None)
                if address:
                    score_dict[address[0]] = score_dict.get(address[0], 0)
                    score_dict[address[0]] += score

                sock.close()