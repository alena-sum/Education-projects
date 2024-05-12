import socket
from _thread import *
from config import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 2345

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as error:
    print(str(error))

s.listen(2)
print("Waiting for a connection...")

current_id = "0"
position = ["mistake:0:0", "mistake:1:0", "choose maze:0:0", "choose maze:1:0", "start:0:0", "start:1:0", "finish:0:0",
            "finish:1:0", "name:0:user1", "name:1:user2", "time:0:0", "time:1:0"]
def threaded_client(user):
    global current_id, position
    user.send(str.encode(current_id))
    current_id = "1"
    reply = ''
    while True:
        data = user.recv(POCKET_SIZE)
        reply = data.decode("utf-8")
        if not data:
            user.send(str.encode("Goodbye!"))
            break
        else:
            print("Recieved: " + reply)
            arr = reply.split(":")
            command = arr[0]
            id = arr[1]
            for i in range(len(position)):
                if command + ':' + id in position[i]:
                    position[i] = reply
                    break
            new_id = None
            if id == "0":
                new_id = "1"
            if id == "1":
                new_id = "0"
            for i in range(len(position)):
                if command + ':' + new_id in position[i]:
                    reply = position[i]
                    break
            print("Sending: " + reply)

        user.sendall(str.encode(reply))
    print("Connection closed.")
    user.close()

while True:
    user, address = s.accept()
    print("Connected to: ", address)

    start_new_thread(threaded_client, (user,))
