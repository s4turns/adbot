import socket
import ssl
import time

# Server and channel settings
server = "irc.efnet.org"  # Change this to the IRC server you want to connect to
port = 6697
channel = "#dnsk"         # Change this to the channel you want to join
nickname = "fucknugget"           # Change this to your bot's nickname

# Multiline message
message = """
 ┬┬─┐┌─┐ ┌┐ ┬  ┌─┐┬┌─┌┐┌┌┬┐ ┌┐┌┌─┐┌┬┐
 │├┬┘│   ├┴┐│  │  ├┴┐│││ ││ │││├┤  │ 
 ┴┴└─└─┘o└─┘┴─┘└─┘┴ ┴┘└┘─┴┘o┘└┘└─┘ ┴ 
🍺 BLCKND IRC Network 
🍺 irc.blcknd.network +6697
🍺 ipv4 + ipv6 + ssl"""

def connect_and_send_message(server, port):
    ssl_sock = None
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created.")

        # Set a timeout for the socket
        sock.settimeout(30)
        print("Timeout set.")

        # Wrap the socket with SSL, ignoring certificate verification
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        ssl_sock = context.wrap_socket(sock, server_hostname=server)
        print("SSL context created with certificate verification disabled.")

        # Connect to the IRC server
        print(f"Connecting to {server} on port {port}...")
        ssl_sock.connect((server, port))
        print("Connected to the server.")

        # Send user info
        print("Sending user info...")
        ssl_sock.sendall(f"NICK {nickname}\r\n".encode('utf-8'))
        ssl_sock.sendall(f"USER {nickname} 0 * :{nickname}\r\n".encode('utf-8'))
        print("User info sent.")

        # Wait a fixed time to ensure the connection is established
        wait_time = 25  # Adjust this wait time as necessary
        print(f"Waiting for {wait_time} seconds to ensure connection is established...")
        time.sleep(wait_time)

        # Join the specified channel
        print(f"Joining channel {channel}...")
        ssl_sock.sendall(f"JOIN {channel}\r\n".encode('utf-8'))

        # Wait a bit to ensure we have joined the channel
        time.sleep(2)

        # Send each line of the multiline message to the channel
        for line in message.split('\n'):
            msg = f"PRIVMSG {channel} :{line.strip()}"
            print(f"Sending message: {msg}")
            ssl_sock.sendall(f"{msg}\r\n".encode('utf-8'))
            time.sleep(1)  # Short delay between lines

        # Quit the server
        print("Quitting the server...")
        ssl_sock.sendall("QUIT :Goodbye!\r\n".encode('utf-8'))

    except socket.timeout:
        print("Socket timeout occurred. Unable to connect to the server.")
    except ssl.SSLError as e:
        print(f"SSL error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        if ssl_sock:
            try:
                print("Closing the socket.")
                ssl_sock.close()
            except Exception as e:
                print(f"Error closing the socket: {e}")

# Try connecting to the server
connect_and_send_message(server, port)
