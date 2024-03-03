import socket
import json
import ssl

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.1.20.33', 12345))

ssl_client_socket = ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_TLS)

question = ssl_client_socket.recv(1024).decode()
question_data = json.loads(question)

print(question_data['question'])
for i, option in enumerate(question_data['options']):
    print(f"{i + 1}. {option}")

user_answer = input("Enter your answer: ")

ssl_client_socket.send(user_answer.encode())

score = ssl_client_socket.recv(1024).decode()
print(f"Your score is: {score}")

ssl_client_socket.close()