import socket
import os


# Function to get files from a directory (no file explorer on client side)
def get_files_from_directory(directory):
    file_list = []
    print(f"Checking directory: {directory}")
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return file_list
    # Walk through the directory and collect file paths
    for root, dirs, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)  # Full path of the file
            file_list.append(full_path)
    return file_list


# Function to send the list of files to the server
def client_send_file_list():
    # Set the server's IP address and port
    server_address = ('192.168.2.83', 9000)  # Replace with actual server IP
    # Directory to send files from (set the path here)
    directory = r'C:\Users\Yonatan Bityaev\OneDrive\Documents'  # Change to a smaller directory
    # Get the list of files from the selected directory
    file_list = get_files_from_directory(directory)
    if not file_list:
        print("No files found in the directory.")
        return
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_address)
        print("Connected to the server.")
        # Convert the list to a string and send it to the server
        file_list_str = "\n".join([os.path.basename(file) for file in file_list])  # Only send file names
        client_socket.sendall(file_list_str.encode('utf-8'))
        print(f"Sent {len(file_list)} files to the server.")
    except Exception as e:
        print(f"Error during connection: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    # Run the client to send the list of files
    client_send_file_list()