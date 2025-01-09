import socket
import os


# Function to get directories from a given path
def get_directories(directory):
    dirs = []
    try:
        for root, subdirs, _ in os.walk(directory):
            if root == directory:  # Only immediate directories
                dirs.extend(subdirs)
    except Exception as e:
        print(f"Error while accessing {directory}: {e}")
    return dirs

# Function to send the directories to the server
def client_send_data(directory):
    # Set the server's IP address and port
    server_address = ('192.168.2.83', 9000)  # Replace with actual server IP

    # Get directories in the specified path
    directories = get_directories(directory)

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_address)
        print("Connected to server.")

        # Send directories to server
        message = f"USERDIRECTORY:{directory}\n" + "\n".join(directories)  # Send directory name and its subdirectories
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent directory {directory} and its subdirectories to server.")

    except Exception as e:
        print(f"Error during connection: {e}")
    finally:
        client_socket.close()


# Initial directory to show is "C:/Users"
if __name__ == "__main__":
    initial_directory = r'C:\Users'  # The starting directory to show (user directories)
    client_send_data(initial_directory)
