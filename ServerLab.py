import Chart as ch
import ManageFile as MF
import socket
import pickle
import struct
import threading
import constants
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = constants.IP_SERVER


def getExt(fmt: str):
    return "." + fmt.lower()


def transactions(filenames, operationType):
    price, newPrice = MF.editCSV(filenames, operationType)
    return price, newPrice


def imageSendData(filename, fmt):
    chart_json = ch.fileToChart(filename, fmt)
    # frame = cv2.imread(image_path)
    data = pickle.dumps(chart_json)

    message_size = struct.pack("L", len(data))

    return message_size, data


def requestData(reqCmd: list):
    if len(reqCmd) == 7:
        return reqCmd[2], reqCmd[4], reqCmd[6]
    else:
        return "H1", reqCmd[2], reqCmd[4]


def requestTransactionInfo(reqCmd: list):
    return reqCmd[2], reqCmd[3]


def listFiles(directory):
    files = ""
    name_set = set()
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            filename = filename.split(".")[0]
            filename = filename.split("_")[0]
            if filename not in name_set:
                files += filename+"\n"
                name_set.add(filename)
    return files, name_set


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
            print("Command by client: " + remote_string)

            period, fmt, par = requestData(remote_command)
            ext = getExt(fmt)
            filename = par + "_" + period

            size, response = imageSendData("data/" + filename + ext, fmt)

            print("Sending image...")
            client_connection.sendall(size + response)
            print("Image Sent")

        elif (command == constants.BUY):
            print("Command by client: " + remote_string)
            par, amount = requestTransactionInfo(remote_command)

            operationType = "BUY"
            price, newPrice = transactions(par, operationType)
            response = "You bought at: " + \
                str(price) + " and The current price of the stock is: " + \
                str(newPrice) + " ↑"
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))
            message = ""

            for x in range(1, len(remote_command)):
                message += remote_command[x]+" "
            print("Este es el mensaje que el cliente envió: "+message)

        elif (command == constants.SELL):
            print("Command by client: " + remote_string)
            par, amount = requestTransactionInfo(remote_command)

            operationType = "SELL"
            price, newPrice = transactions(par, operationType)
            response = "You sold at: " + \
                str(price) + " and The current price of the stock is: " + \
                str(newPrice) + " ↓"
            client_connection.sendall(
                response.encode(constants.ENCONDING_FORMAT))
            message = ""

            for x in range(1, len(remote_command)):
                message += remote_command[x]+" "
            print("Este es el mensaje que el cliente envió: "+message)

        elif (command == constants.LIST):
            available, _ = listFiles('data')
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
        try:
            client_connection, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handler_client_connection, args=(client_connection, client_address))
            client_thread.start()
        except KeyboardInterrupt:
            server_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()
            print("closed")
            break

    print('Socket is closed...')
    server_socket.close()


if __name__ == "__main__":
    main()
