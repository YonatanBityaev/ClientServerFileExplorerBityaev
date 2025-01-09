import socket
import tkinter as tk
from tkinter import Listbox, Scrollbar, messagebox


# Function to display the directory structure (drives and directories)
def display_file_structure(data):
    if not data:
        messagebox.showinfo("No Data", "No data received from the client.")
        return

    # Create a Tkinter window to display the data
    window = tk.Tk()
    window.title("Client's File Explorer")
    window.geometry('600x400')  # Set window size (width x height)
    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())  # Center window

    # Add a header label to make the UI more friendly
    header_label = tk.Label(window, text="Client's File Explorer", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
    header_label.pack(fill=tk.X)

    # Create a frame to hold the Listbox and Scrollbar together
    frame = tk.Frame(window)
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Create the Listbox to display the drives and directories
    listbox = Listbox(frame, width=50, height=15, font=("Arial", 10), bg="#f0f0f0", fg="#333", selectmode=tk.SINGLE, bd=2, relief="groove")
    listbox.pack(side="left", fill=tk.BOTH, expand=True)

    # Create the Scrollbar for the Listbox
    scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    # Link the scrollbar to the listbox
    listbox.config(yscrollcommand=scrollbar.set)

    # Insert the received data into the Listbox
    for item in data:
        listbox.insert(tk.END, item)

    # Add a button to close the window
    close_button = tk.Button(window, text="Close", font=("Arial", 12), bg="#FF6347", fg="white", command=window.quit)
    close_button.pack(pady=10)

    # Start the Tkinter event loop to display the window
    window.mainloop()

# Set up the server socket to listen for connections
def server_receive_data():
    # Set up the server's IP address and port
    server_address = ('0.0.0.0', 9000)  # 'localhost' or use the actual IP if needed

    # Create the socket and bind it to the address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Bind the server to the address and port
        server_socket.bind(server_address)
        print(f"Server binding successful at {server_address}")
    except Exception as e:
        print(f"Error binding server: {e}")
        return

    # Listen for incoming connections
    server_socket.listen(1)
    print("Waiting for client connection...")

    try:
        connection, client_address = server_socket.accept()
        print(f"Connection established with: {client_address}")
        data = b""

        while True:
            data_chunk = connection.recv(1024)
            if not data_chunk:
                break
            data += data_chunk

        if data:
            # Decode the received data
            message = data.decode('utf-8')
            print(f"Received data: {message}")

            # Process the received data
            lines = message.split("\n")
            drive = None
            subdirs = []

            for line in lines:
                if line.startswith("DRIVE:"):
                    if drive and subdirs:
                        # Show previous drive's subdirectories
                        display_file_structure(subdirs)
                    drive = line.split(":")[1].strip()  # Get the drive
                    subdirs = []
                elif line.strip():
                    subdirs.append(line.strip())

            if drive and subdirs:
                # Show the last drive's subdirectories
                display_file_structure(subdirs)

    except Exception as e:
        print(f"Error during connection handling: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    # Run the server to receive the file structure
    server_receive_data()
