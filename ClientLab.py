import socket
import pickle
import struct
import constants
from Parser import *
from plotly.io import from_json
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receive_json(name, data, msg_size):
    print("Chart received")
    frame_data = data[:msg_size]
    data = data[msg_size:]

    json_data = pickle.loads(frame_data)

    fig = from_json(json_data)
    fig.show()


def main():
    print('***********************************')
    print('Client is running...')
    client_socket.connect(("127.0.0.1", constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands:')
    command_to_send = input()
    list_commands = command_to_send.split()

    while command_to_send != constants.QUIT:
        data_received = ""
        data_received = data_received.encode(constants.ENCONDING_FORMAT)
        if command_to_send == '':
            print('Please input a valid command...')

        elif (list_commands[0] == constants.REQ):
            try:
                reqStructure(list_commands)
            except Exception as e:
                print("\033[91mBad structure of command:\033[0m", e)
                command_to_send = input()
                list_commands = command_to_send.split()
                continue

            client_socket.send(
                bytes(command_to_send, constants.ENCONDING_FORMAT))
            print("Loading image....")
            data = b''
            payload_size = struct.calcsize('L')

            while len(data) < payload_size:
                data += client_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack('L', packed_msg_size)[0]
            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += client_socket.recv(4096)

            img_name = list_commands[-1]
            receive_json(img_name, data, msg_size)


        elif (list_commands[0] == constants.BUY):
            try:
                buyStructure(list_commands)
                client_socket.send(
                    bytes(command_to_send, constants.ENCONDING_FORMAT))
            except Exception as e:
                print("\033[91mBad structure of command:\033[0m", e)

        elif (list_commands[0] == constants.SELL):
            try:
                buyStructure(list_commands)
                client_socket.send(
                    bytes(command_to_send, constants.ENCONDING_FORMAT))
            except Exception as e:
                print("\033[91mBad structure of command:\033[0m", e)

        elif (list_commands[0] == constants.LIST):
            try:
                client_socket.send(
                    bytes(command_to_send, constants.ENCONDING_FORMAT))
                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            except Exception as e:
                print(e)

        elif (list_commands[0] == constants.HELP):
            try:
                client_socket.send(
                    bytes(command_to_send, constants.ENCONDING_FORMAT))
                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            except Exception as e:
                print(e)

        else:
            client_socket.send(
                bytes(command_to_send, constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)

        print(type(data_received))
        print(data_received.decode(constants.ENCONDING_FORMAT))
        command_to_send = input()
        list_commands = command_to_send.split()
    client_socket.send(bytes(command_to_send, constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()


if __name__ == '__main__':
    main()
