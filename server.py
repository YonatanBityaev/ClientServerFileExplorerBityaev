import socket
import tkinter as tk
from tkinter import ttk, messagebox
from client import client_send_data


# Function to display directories and files in a Treeview
def display_file_structure(data, parent=None):
    if not data:
        messagebox.showinfo("No Data", "No data received from the client.")
        return

    # Create a Tkinter window to display the data
    window = tk.Tk() if parent is None else parent
    window.title("Client's File Explorer")
    window.geometry('800x600')
    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())

    # Add a header label to make the UI more friendly
    header_label = tk.Label(window, text="Client's File Explorer", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
    header_label.pack(fill=tk.X)

    # Create a Treeview widget to display directories and files
    tree = ttk.Treeview(window)
    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Add a scrollbar for the Treeview
    scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Configure columns
    tree["columns"] = ("Type")
    tree.heading("#0", text="Name", anchor="w")
    tree.heading("Type", text="Type", anchor="w")
    tree.column("#0", stretch=tk.YES)
    tree.column("Type", width=100, stretch=tk.NO)

    # Insert data into the Treeview
    def populate_tree(parent_node, path_data):
        for item in path_data:
            if item.startswith("[DIR]"):
                folder_name = item.replace("[DIR] ", "")
                folder_node = tree.insert(parent_node, "end", text=folder_name, values=("Folder",))
                # You could add a mechanism to load subdirectories dynamically when expanded
            else:
                tree.insert(parent_node, "end", text=item, values=("File",))

    # Parse the received data and populate the Treeview
    root_directory = data[0]  # Assume the first item is the root directory name
    tree_root = tree.insert("", "end", text=root_directory, values=("Root",))
    populate_tree(tree_root, data[1:])  # Populate the tree starting from the second line

    # Add an event to handle double-clicking to explore further
    def on_double_click(event):
        selected_item = tree.selection()[0]
        item_text = tree.item(selected_item, "text")
        if "Folder" in tree.item(selected_item, "values"):
            print(f"Selected folder: {item_text}")
            client_send_data(item_text)  # Send the selected folder to the server

    tree.bind("<Double-1>", on_double_click)

    # Add a button to close the window
    close_button = tk.Button(window, text="Close", font=("Arial", 12), bg="#FF6347", fg="white", command=window.quit)
    close_button.pack(pady=10)

    window.mainloop()


# Set up the server socket to listen for connections
def server_receive_data():
    server_address = ('0.0.0.0', 9000)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(server_address)
        print(f"Server binding successful at {server_address}")
    except Exception as e:
        print(f"Error binding server: {e}")
        return

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
            message = data.decode('utf-8')
            print(f"Received data: {message}")
            lines = message.split("\n")
            if lines[0].startswith("USERDIRECTORY:"):
                root_directory = lines[0].split(":")[1].strip()
                directories = [root_directory] + lines[1:]
                display_file_structure(directories)

    except Exception as e:
        print(f"Error during connection handling: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    server_receive_data()
