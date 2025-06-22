import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = "bmi_history.csv"

# ========== BMI Classification ==========
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# ========== Save BMI to CSV ==========
def save_bmi(name, height, weight, bmi, category):
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, height, weight, f"{bmi:.2f}", category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# ========== Load History ==========
def load_history(name_filter=None):
    records = []
    if not os.path.exists(DATA_FILE):
        return records
    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if name_filter is None or row[0] == name_filter:
                records.append(row)
    return records

# ========== Calculate BMI ==========
def calculate_bmi():
    try:
        name = name_entry.get().strip()
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if not name:
            raise ValueError("Name cannot be empty.")
        if not (50 <= height <= 250) or not (10 <= weight <= 300):
            raise ValueError("Height/Weight out of realistic range.")

        height_m = height / 100
        bmi = weight / (height_m ** 2)
        category = classify_bmi(bmi)

        result_label.config(text=f"BMI: {bmi:.2f} ({category})")

        save_bmi(name, height, weight, bmi, category)

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception:
        messagebox.showerror("Error", "An unexpected error occurred.")

# ========== Show History ==========
def show_history():
    name = name_entry.get().strip()
    records = load_history(name if name else None)
    if not records:
        messagebox.showinfo("History", "No records found.")
        return

    history_window = tk.Toplevel(app)
    history_window.title("BMI History")
    history_window.geometry("600x300")

    columns = ("Name", "Height", "Weight", "BMI", "Category", "Timestamp")
    tree = ttk.Treeview(history_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for row in records:
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)

# ========== Show Graph ==========
def show_graph():
    name = name_entry.get().strip()
    records = load_history(name if name else None)
    if not records:
        messagebox.showinfo("Graph", "No data available to plot.")
        return

    dates = [datetime.strptime(r[5], "%Y-%m-%d %H:%M:%S") for r in records]
    bmi_values = [float(r[3]) for r in records]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmi_values, marker='o', linestyle='-', color='blue')
    plt.title(f'BMI Trend {"for " + name if name else ""}')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()
    plt.show()

# ========== GUI ==========
app = tk.Tk()
app.title("Advanced BMI Calculator")
app.geometry("400x450")
app.config(bg="#eef5f6")

tk.Label(app, text="Advanced BMI Calculator", font=("Arial", 16, "bold"), bg="#eef5f6").pack(pady=10)

tk.Label(app, text="Name:", bg="#eef5f6").pack()
name_entry = tk.Entry(app, font=("Arial", 12))
name_entry.pack(pady=5)

tk.Label(app, text="Height (cm):", bg="#eef5f6").pack()
height_entry = tk.Entry(app, font=("Arial", 12))
height_entry.pack(pady=5)

tk.Label(app, text="Weight (kg):", bg="#eef5f6").pack()
weight_entry = tk.Entry(app, font=("Arial", 12))
weight_entry.pack(pady=5)

tk.Button(app, text="Calculate BMI", command=calculate_bmi, font=("Arial", 12, "bold")).pack(pady=10)

result_label = tk.Label(app, text="BMI: --", font=("Arial", 14), bg="#eef5f6", fg="black")
result_label.pack(pady=10)

tk.Button(app, text="View History", command=show_history).pack(pady=5)
tk.Button(app, text="Show Graph", command=show_graph).pack(pady=5)

app.mainloop()
