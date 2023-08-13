



import socket
import constants
from Parser import *
import os
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def receive_image(name):
    image_data = client_socket.recv(constants.RECV_BUFFER_SIZE)
    downloads_directory = os.path.expanduser("~/Downloads")
    image_path = os.path.join(downloads_directory,name+'.jpg')

    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)

    print(f'Image received and saved as "{image_path}"')
def main():
    print('***********************************')
    print('Client is running...')
    client_socket.connect(("127.0.0.1",constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands:')
    command_to_send = input()
    list_commands= command_to_send.split()
    
    while command_to_send != constants.QUIT:
        if command_to_send == '':
            print('Please input a valid command...')
            command_to_send = input()                        
        elif (list_commands[0] == constants.REQ):
            try:
              reqStructure(list_commands)
              client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
              receive_image('prueba')
              
            except Exception as e:
              print("\033[91mBad structure of command:\033[0m",e)
            command_to_send = input()
            list_commands= command_to_send.split()
        elif (list_commands[0] == constants.BUY):
            try:
              buyStructure(list_commands)
              client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            except Exception as e:
              print("\033[91mBad structure of command:\033[0m",e)
            command_to_send = input()
            list_commands= command_to_send.split()
        elif (list_commands[0] == constants.SELL):
            try:
              buyStructure(list_commands)
              client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            except Exception as e:
              print("\033[91mBad structure of command:\033[0m",e)
            command_to_send = input()
            list_commands= command_to_send.split()  
        elif (list_commands[0] == constants.LIST):
            try:
              client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
              data_received = client_socket.recv(constants.RECV_BUFFER_SIZE) 
            except Exception as e:
              print(e)
            command_to_send = input()
            list_commands= command_to_send.split()               
        else:        
            client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()
    
    client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()    

if __name__ == '__main__':
    main()