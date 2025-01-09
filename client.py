import socket
import os


# Function to get drives in the system
def get_drives():
    drives = []
    for drive in range(65, 91):  # Letters A to Z
        drive_letter = chr(drive) + ":\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives

# Function to get directories and subdirectories from a given directory
def get_directories(directory):
    dirs = []
    try:
        for root, subdirs, _ in os.walk(directory):
            if root == directory:  # Only immediate directories
                dirs.extend(subdirs)
    except Exception as e:
        print(f"Error while accessing {directory}: {e}")
    return dirs

# Function to send the drives and directories to the server
def client_send_data():
    # Set the server's IP address and port
    server_address = ('192.168.2.83', 9000)  # Replace with actual server IP

    # Get drives on the client machine
    drives = get_drives()

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_address)
        print("Connected to server.")

        # Send the drives first
        for drive in drives:
            directories = get_directories(drive)
            message = f"DRIVE:{drive}\n" + "\n".join(directories)  # Send drive and its directories
            client_socket.sendall(message.encode('utf-8'))
            print(f"Sent drive: {drive} and directories to server.")

    except Exception as e:
        print(f"Error during connection: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    client_send_data()
