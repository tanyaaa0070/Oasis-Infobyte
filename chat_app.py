# === ALL-IN-ONE ADVANCED CHAT APPLICATION ===
# Features: GUI, login/register, encryption, emojis, image sharing

import socket
import threading
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import base64
import json
import os
from cryptography.fernet import Fernet
import io

# === Configuration ===
HOST = "127.0.0.1"
PORT = 5555
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# === Global Variables ===
clients = []
USERNAME = ""
client_socket = None

# === Server Code ===
def start_server():
    def handle_client(sock):
        while True:
            try:
                msg = sock.recv(4096)
                if msg:
                    for client in clients:
                        if client != sock:
                            client.send(msg)
            except:
                clients.remove(sock)
                break

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("[SERVER] Listening on", HOST, PORT)

    def accept_clients():
        while True:
            client, addr = server.accept()
            print("[NEW CONNECTION]", addr)
            clients.append(client)
            thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
            thread.start()

    threading.Thread(target=accept_clients, daemon=True).start()

# === Authentication ===
def authenticate():
    global USERNAME
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({}, f)

    users = json.load(open("users.json"))
    choice = simpledialog.askstring("Login/Register", "Type 'login' or 'register'")
    USERNAME = simpledialog.askstring("Username", "Enter username")
    password = simpledialog.askstring("Password", "Enter password")

    if choice == "register":
        users[USERNAME] = password
        with open("users.json", "w") as f:
            json.dump(users, f)
    elif choice == "login":
        if users.get(USERNAME) != password:
            messagebox.showerror("Login Failed", "Invalid credentials")
            exit()
    else:
        exit()

# === Send and Receive ===
def send_message():
    msg = input_field.get()
    if msg:
        enc = cipher.encrypt(f"{USERNAME}: {msg}".encode())
        client_socket.send(enc)
        input_field.delete(0, tk.END)
        with open("message_log.txt", "a") as f:
            f.write(f"{USERNAME}: {msg}\n")

def send_image():
    path = filedialog.askopenfilename()
    if path:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
            msg = f"{USERNAME} [img]:{data}"
            enc = cipher.encrypt(msg.encode())
            client_socket.send(enc)

# === Receive Function ===
def receive():
    while True:
        try:
            msg = client_socket.recv(4096)
            msg = cipher.decrypt(msg).decode()
            if "[img]:" in msg:
                sender, imgdata = msg.split(" [img]:")
                img = Image.open(io.BytesIO(base64.b64decode(imgdata)))
                img = img.resize((120, 120))
                img = ImageTk.PhotoImage(img)
                chat_box.image_create(tk.END, image=img)
                chat_box.insert(tk.END, f"\n{sender} sent an image.\n")
                chat_box.image = img
            else:
                chat_box.insert(tk.END, f"{msg}\n")
        except Exception as e:
            print("[ERROR]", e)
            break

# === GUI Setup ===
def launch_gui():
    global input_field, chat_box
    app = tk.Tk()
    app.title("Chat App")
    app.geometry("400x500")

    chat_box = tk.Text(app, wrap="word")
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    input_field = tk.Entry(app, font=("Arial", 12))
    input_field.pack(padx=10, pady=5, fill=tk.X)

    frame = tk.Frame(app)
    frame.pack()

    tk.Button(frame, text="Send", command=send_message).pack(side="left", padx=5)
    tk.Button(frame, text="📷", command=send_image).pack(side="left")

    threading.Thread(target=receive, daemon=True).start()
    app.mainloop()

# === Main ===
if __name__ == "__main__":
    mode = simpledialog.askstring("Mode", "Type 'server' or 'client'")
    if mode == "server":
        start_server()
        tk.Tk().mainloop()  # Keep window open
    elif mode == "client":
        authenticate()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        launch_gui()
    else:
        print("Invalid mode")
