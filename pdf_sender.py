import requests
import importlib.util
import os
import shutil

spec = importlib.util.spec_from_file_location("config", "tools/config.py")
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


def get_token(username, password, host, port):
    # login to the server and get the token
    address = f"http://{host}:{port}/login"

    # put the username and password in the body of the request
    body = {"username": username, "password": password}
    # send the request
    try:
        response = requests.post(address, data=body).text
    except:
        print("Error in connecting to the server")
        return None

    # make dictionary from the response
    response = eval(response)
    token = response['token']
    return token


# read config and extract username and password and port and host
ports = []
hosts = []
usernames = []
passwords = []
tokens = []

config1 = config.read_config()
username1 = config1["printer_server1_username"]
password1 = config1["printer_server1_password"]
port1 = config1["printer_server1_port"]
host1 = config1["printer_server1_host"]

config2 = config.read_config()
username2 = config2["printer_server2_username"]
password2 = config2["printer_server2_password"]
port2 = config2["printer_server2_port"]
host2 = config2["printer_server2_host"]

# append username and password and port and host to the lists
usernames.append(username1)
passwords.append(password1)
ports.append(port1)
hosts.append(host1)

usernames.append(username2)
passwords.append(password2)
ports.append(port2)
hosts.append(host2)


token1 = get_token(username1, password1, host1, port1)
token2 = get_token(username2, password2, host2, port2)
tokens.append(token1)
tokens.append(token2)


while True:
    # read the pdf files in the to_send_files folder
    files = [i for i in os.listdir("to_send_files") if i.endswith(".pdf")]

    if len(files) == 0:
        continue
    
    selected_printer = 0
    selected_printer_files = 100
    # choose between servers
    for i in range(len(tokens)):
        # check which server has less files to print
        address = f"http://{hosts[i]}:{ports[i]}/check"
        header = {'x-access-token': tokens[i]}

        # make a get request
        response = requests.get(address, headers=header).text
        response = eval(response)
        if response['number_of_files'] < selected_printer_files:
            selected_printer = i
            selected_printer_files = response['number_of_files']

    host = hosts[selected_printer]
    port = ports[selected_printer]
    token = tokens[selected_printer]

    # send the first file
    file = files[0]
    address = f"http://{host}:{port}/print"
    files = {'file': open(f"to_send_files/{file}", 'rb')}
    headers = {'x-access-token': token}

    # send the request
    response = requests.post(address, files=files, headers=headers).text

    if "has recieved" in response:
        # copy the file to the sent_files folder
        shutil.copy(f"to_send_files/{file}", f"sent_files/{file}")

        # remove the file from the to_send_files folder
        os.remove(f"to_send_files/{file}")


