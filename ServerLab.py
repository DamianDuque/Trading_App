import Chart as ch
import socket
import threading
import constants
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = constants.IP_SERVER


def imageSendData(filename):
    image_path = 'data/'+filename+'.png'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return image_data


def listFiles(directory):
    files = ""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files += filename+"\n"
    return files


def main():
    print("***********************************")
    print("Server is running...")
    print("Dir IP:", server_address)
    print("Port:", constants.PORT)
    server_execution()

# Handler for manage incomming clients conections...


def handler_client_connection(client_connection, client_address):
    print(
        f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')

    is_connected = True
    while is_connected:
        data_recevived = client_connection.recv(constants.RECV_BUFFER_SIZE)

        if not data_recevived:
            is_connected = False
        remote_string = str(data_recevived.decode(constants.ENCONDING_FORMAT))
        remote_command = remote_string.split()
        command = remote_command[0]
        print(f'Data received from: {client_address[0]}:{client_address[1]}')

        if (command == constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))
            is_connected = False

        elif (command == constants.REQ):
            response = imageSendData('descarga')
            client_connection.sendall(response)
            message = ""
            for x in range(1, len(remote_command)):
                message += remote_command[x]+" "
            print("Command by client: "+message)

        elif (command == constants.BUY):
            response = "Successful purchase"
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))
            message = ""

            for x in range(1, len(remote_command)):
                message += remote_command[x]+" "
            print("Este es el mensaje que el cliente envió: "+message)

        elif (command == constants.SELL):
            response = "Successful sale"
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))
            message = ""

            for x in range(1, len(remote_command)):
                message += remote_command[x]+" "
            print("Este es el mensaje que el cliente envió: "+message)

        elif (command == constants.LIST):
            available = listFiles('data')
            response = "-----Available PAR-----\n"+available+"-----"
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))

        elif (command == constants.HELP):
            with open("help.txt", 'r', newline='') as f:
                response = f.read()
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))

        else:
            response = '400 BCMD\n\rCommand-Description: Bad command\n\r'
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))

    print(
        f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()

# Function to start server process...


def server_execution():
    tuple_connection = (server_address, constants.PORT)
    server_socket.bind(tuple_connection)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket is bind to address and port...')
    server_socket.listen(5)
    print('Socket is listening...')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(
            target=handler_client_connection, args=(client_connection, client_address))
        client_thread.start()

    print('Socket is closed...')
    server_socket.close()


if __name__ == "__main__":
    main()
