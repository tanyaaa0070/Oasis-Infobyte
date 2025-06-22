import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip

# ========== Password Generation Logic ==========
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showwarning("Invalid Length", "Password length should be at least 4.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for length.")
        return

    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    exclude_chars = exclude_entry.get()

    if not any([use_upper, use_lower, use_digits, use_symbols]):
        messagebox.showerror("Error", "Select at least one character type.")
        return

    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    # Exclude unwanted characters
    for ch in exclude_chars:
        char_pool = char_pool.replace(ch, "")

    if len(char_pool) == 0:
        messagebox.showerror("Error", "No characters left to generate password.")
        return

    password = ''.join(random.choice(char_pool) for _ in range(length))
    password_var.set(password)

# ========== Copy to Clipboard ==========
def copy_to_clipboard():
    password = password_var.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# ========== GUI ==========
app = tk.Tk()
app.title("Advanced Password Generator")
app.geometry("400x450")
app.config(bg="#f0f4f8")

tk.Label(app, text="Advanced Password Generator", font=("Arial", 16, "bold"), bg="#f0f4f8").pack(pady=10)

# Password length
tk.Label(app, text="Password Length:", bg="#f0f4f8", font=("Arial", 12)).pack()
length_entry = tk.Entry(app, font=("Arial", 12), width=10, justify="center")
length_entry.pack(pady=5)
length_entry.insert(0, "12")

# Checkboxes
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(app, text="Include Uppercase", variable=upper_var, bg="#f0f4f8").pack(anchor="w", padx=50)
tk.Checkbutton(app, text="Include Lowercase", variable=lower_var, bg="#f0f4f8").pack(anchor="w", padx=50)
tk.Checkbutton(app, text="Include Digits", variable=digits_var, bg="#f0f4f8").pack(anchor="w", padx=50)
tk.Checkbutton(app, text="Include Symbols", variable=symbols_var, bg="#f0f4f8").pack(anchor="w", padx=50)

# Exclude characters
tk.Label(app, text="Exclude Characters (optional):", bg="#f0f4f8").pack(pady=5)
exclude_entry = tk.Entry(app, font=("Arial", 12), width=20, justify="center")
exclude_entry.pack(pady=5)

# Generate Button
tk.Button(app, text="Generate Password", font=("Arial", 12, "bold"), command=generate_password).pack(pady=10)

# Output
password_var = tk.StringVar()
tk.Entry(app, textvariable=password_var, font=("Arial", 14), width=30, justify="center", state="readonly").pack(pady=5)

tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)

app.mainloop()
