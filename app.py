
import os
import sys
import shutil
import subprocess
import tkinter as tk

from tkinter import ttk, filedialog, messagebox
import pandas as pd


# ---------------- PROJECT PATHS ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPT = os.path.join(BASE_DIR, "clean_titanic.py")
RAW = os.path.join(BASE_DIR, "titanic_raw.csv")
CLEAN = os.path.join(BASE_DIR, "titanic_cleaned.csv")
SHOTS = os.path.join(BASE_DIR, "screenshots")


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Titanic Data Cleaning Application")
root.geometry("1050x700")
root.minsize(850, 600)
root.configure(bg="#f1f5f9")


# ---------------- COLORS ----------------

BG = "#f1f5f9"
NAVY = "#172554"
BLUE = "#2563eb"
WHITE = "#ffffff"
GREEN = "#15803d"


# ---------------- VARIABLES ----------------

selected_file = tk.StringVar(value="No dataset selected")
status = tk.StringVar(value="Ready")


# ---------------- TITLE ----------------

header = tk.Frame(root, bg=NAVY, height=85)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="TITANIC DATA CLEANING",
    font=("Arial", 22, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(15, 2))

tk.Label(
    header,
    text="Python | Pandas | NumPy | Matplotlib | Seaborn",
    font=("Arial", 10),
    bg=NAVY,
    fg="#bfdbfe"
).pack()


# ---------------- MAIN CONTENT ----------------

main = tk.Frame(root, bg=BG, padx=20, pady=20)
main.pack(fill="both", expand=True)


# ---------------- FILE SELECTION ----------------

file_frame = tk.LabelFrame(
    main,
    text="  Dataset Selection  ",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    padx=15,
    pady=15
)
file_frame.pack(fill="x", pady=(0, 15))


tk.Label(
    file_frame,
    textvariable=selected_file,
    bg=WHITE,
    fg="#475569",
    font=("Arial", 10)
).pack(side="left", fill="x", expand=True)


# ---------------- DATA PREVIEW ----------------

preview_frame = tk.LabelFrame(
    main,
    text="  Dataset Preview  ",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    padx=10,
    pady=10
)
preview_frame.pack(fill="both", expand=True, pady=(0, 15))


table_container = tk.Frame(preview_frame)
table_container.pack(fill="both", expand=True)

tree = ttk.Treeview(
    table_container,
    show="headings",
    height=8
)

yscroll = ttk.Scrollbar(
    table_container,
    orient="vertical",
    command=tree.yview
)

xscroll = ttk.Scrollbar(
    table_container,
    orient="horizontal",
    command=tree.xview
)

tree.configure(
    yscrollcommand=yscroll.set,
    xscrollcommand=xscroll.set
)

tree.grid(row=0, column=0, sticky="nsew")
yscroll.grid(row=0, column=1, sticky="ns")
xscroll.grid(row=1, column=0, sticky="ew")

table_container.rowconfigure(0, weight=1)
table_container.columnconfigure(0, weight=1)


# ---------------- FUNCTIONS ----------------

def preview_dataset(path):

    try:
        df = pd.read_csv(path)

        tree.delete(*tree.get_children())

        tree["columns"] = list(df.columns)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=110, minwidth=80)

        for _, row in df.head(5).iterrows():
            tree.insert(
                "",
                "end",
                values=[
                    str(value)[:40] for value in row
                ]
            )

        status.set(
            f"Dataset loaded: {df.shape[0]} rows, "
            f"{df.shape[1]} columns"
        )

    except Exception as e:
        messagebox.showerror("Preview Error", str(e))


def select_file():

    path = filedialog.askopenfilename(
        title="Select Titanic CSV Dataset",
        filetypes=[("CSV Files", "*.csv")]
    )

    if path:
        selected_file.set(path)
        preview_dataset(path)


def clean_dataset():

    if selected_file.get() == "No dataset selected":
        messagebox.showwarning(
            "Dataset Required",
            "Please select a CSV dataset first."
        )
        return

    if not os.path.exists(SCRIPT):
        messagebox.showerror(
            "Missing Script",
            "clean_titanic.py was not found."
        )
        return

    try:

        # Copy selected dataset to the expected input path
        shutil.copy2(selected_file.get(), RAW)

        status.set("Cleaning dataset... Please wait.")
        root.update_idletasks()

        result = subprocess.run(
            [sys.executable, SCRIPT],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            messagebox.showerror(
                "Cleaning Failed",
                result.stderr[-3000:] or result.stdout[-3000:]
            )
            status.set("Cleaning failed.")
            return

        output.delete("1.0", tk.END)

        output.insert(
            tk.END,
            result.stdout
        )

        if os.path.exists(CLEAN):
            status.set("Data cleaning completed successfully!")

            # Display cleaned dataset
            preview_dataset(CLEAN)

            messagebox.showinfo(
                "Success",
                "Titanic dataset cleaned successfully!\n\n"
                "Output: titanic_cleaned.csv"
            )

        else:
            status.set("Output file not found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status.set("Error occurred.")


def open_screenshots():

    if os.path.exists(SHOTS):
        os.startfile(SHOTS)
    else:
        messagebox.showwarning(
            "Not Found",
            "Screenshots folder does not exist yet."
        )


def open_output():

    if os.path.exists(CLEAN):
        os.startfile(CLEAN)
    else:
        messagebox.showwarning(
            "Not Found",
            "Please clean the dataset first."
        )


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(main, bg=BG)
button_frame.pack(fill="x", pady=5)


def make_button(parent, text, command, color=BLUE):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=16,
        pady=10,
        cursor="hand2"
    )


make_button(
    button_frame,
    "Select CSV",
    select_file
).pack(side="left", padx=(0, 8))


make_button(
    button_frame,
    "Clean Dataset",
    clean_dataset,
    GREEN
).pack(side="left", padx=8)


make_button(
    button_frame,
    "View Output CSV",
    open_output,
    NAVY
).pack(side="left", padx=8)


make_button(
    button_frame,
    "View Charts",
    open_screenshots,
    "#7c3aed"
).pack(side="left", padx=8)


# ---------------- CLEANING REPORT ----------------

report_frame = tk.LabelFrame(
    main,
    text="  Cleaning Report / Console Output  ",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    padx=10,
    pady=10
)
report_frame.pack(fill="both", expand=True, pady=(10, 5))

output = tk.Text(
    report_frame,
    height=7,
    bg="#0f172a",
    fg="#e2e8f0",
    font=("Consolas", 9),
    wrap="word"
)
output.pack(fill="both", expand=True)

output.insert(
    tk.END,
    "Welcome to Titanic Data Cleaning Application!\n\n"
    "1. Select your CSV dataset.\n"
    "2. Preview the dataset.\n"
    "3. Click Clean Dataset.\n"
    "4. View your cleaning report and output.\n"
)


# ---------------- STATUS BAR ----------------

status_bar = tk.Label(
    root,
    textvariable=status,
    bg="#dbeafe",
    fg=NAVY,
    font=("Arial", 9),
    anchor="w",
    padx=15,
    pady=8
)

status_bar.pack(fill="x")


# ---------------- START APPLICATION ----------------

root.mainloop()
