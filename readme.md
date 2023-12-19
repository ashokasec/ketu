# Ketu: Remote Control and Surveillance Tool

`NOTE: Hey, this tool isn't quite ready for everyone to use. I built it for myself to learn how things work behind the scenes`

Ketu is a tool designed to facilitate remote control and surveillance. It establishes a seamless connection between a server and a client, enabling the exchange of key logs, WIFI passwords, screenshots, clipboard content, and system information. Named after the shadow planet Ketu, this project embodies the enigmatic nature of remote communication.

`Disclaimer: This tool should be used responsibly for educational purposes only. Its use for any malicious activities is strictly discouraged. The developers and contributors are not liable for any misuse. Always respect ethical and legal standards while using this tool.`

![Banner](banner.jpg)

## Features

- Active Keylogging: Captures keystrokes remotely.
- WIFI Passwords: Extracts and shares past connected wireless SSIDs and their passwords.
- Take Screenshot: Captures and shares screenshots without storing them on the client side.
- Copy Clipboard: Allows clients to share clipboard content with the server.
- System Information: Retrieves and displays system information from the client.
- Open Links: Opens Arbitrary Links in Default Browser.
- Notify: Push a custom Notification.

## Getting Started

1. Clone or download this repository.
   ```
   git clone https://github.com/ashokasec/ketu.git
   ```
2. Configure the server by running `server.py` on the host machine.
3. Run `client.py` on the remote machine, specifying the server's IP address using the `--address` argument.
   Note: No need to specify server's IP address, if running on same machine for demo purpose.

   | They will install the requirements by themselves |

## Usage

- Once connected, the server can request various actions from the client using commands.
- Commands include requesting system information, displaying WIFI passwords, capturing screenshots, retrieving clipboard content, and more.
- Active keylogging is set up by default and doesn't require a command to start working.

## Contributions

Contributions are welcome! Feel free to submit pull requests or report issues on the GitHub repository.
