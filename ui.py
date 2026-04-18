import oracledb
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()

class login:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.configure(bg="#1e1e2f")
        self.login_window.geometry("1400x800")
        self.login_window.title("Login credentials")

        l_frame = tk.Frame(self.login_window, bg="#1e1e2f")
        l_frame.pack(pady=40)

        self.username = tk.Label(
            l_frame, text="Username", bg="#1e1e2f", fg="white", font=("Arial", 12)
        )
        self.username.grid(row=0, column=0, pady=10, sticky="w")

        self.username_entry = tk.Entry(
            l_frame, font=("Arial", 12), fg="white",
            bg="#2c2c3e", insertbackground="white"
        )
        self.username_entry.grid(row=0, column=1, pady=10)

        self.password = tk.Label(
            l_frame, text="Password", bg="#1e1e2f", fg="white", font=("Arial", 12)
        )
        self.password.grid(row=1, column=0, pady=10)

        self.password_entry = tk.Entry(
            l_frame, show="*", font=("Arial", 12),
            fg="white", bg="#2c2c3e", insertbackground="white"
        )
        self.password_entry.grid(row=1, column=1, pady=10)

        self.login_button = tk.Button(
            self.login_window, text='Login', command=self.login
        )
        self.login_button.pack(pady=20)

        self.login_window.mainloop()

    # -----------------------------
    # FETCH STOPS FROM DB
    # -----------------------------
    def get_stops(self):
        try:
            conn = oracledb.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dsn=os.getenv("DB_DSN")
            )
            cursor = conn.cursor()

            cursor.execute("SELECT stop_name FROM stops ORDER BY stop_id")
            stops = [row[0] for row in cursor.fetchall()]

            conn.close()
            return stops

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    # -----------------------------
    # LOGIN
    # -----------------------------
    def login(self):
        try:
            conn = oracledb.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dsn=os.getenv("DB_DSN")
            )
            cursor = conn.cursor()

            username = self.username_entry.get()
            password = self.password_entry.get()

            cursor.execute("""
                SELECT * FROM users 
                WHERE name = :1 AND password = :2
            """, (username, password))

            user = cursor.fetchone()

            if user:
                self.show_main_screen()
            else:
                messagebox.showerror("Login Failed", "Invalid Username or password")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -----------------------------
    # MAIN UI
    # -----------------------------
    def show_main_screen(self):
        for widget in self.login_window.winfo_children():
            widget.destroy()

        self.login_window.configure(bg="#eaeaea")

        main_frame = tk.Frame(self.login_window, bg="#eaeaea")
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#eaeaea")
        left_frame.pack(side="left", anchor="nw", padx=20, pady=20)

        # FETCH STOPS ONCE
        stops_list = self.get_stops()

        # TOP ROW
        top_row = tk.Frame(left_frame, bg="#eaeaea")
        top_row.pack(pady=20)

        # START STOP
        start_box = tk.Frame(top_row, bg="white", bd=2, relief="solid")
        start_box.grid(row=0, column=0, padx=20, ipadx=20, ipady=10)

        tk.Label(start_box, text="Start Stop", font=("Arial", 14), bg="white").pack()

        self.start_var = tk.StringVar()
        self.start_dropdown = ttk.Combobox(
            start_box,
            textvariable=self.start_var,
            values=stops_list,
            state="readonly",
            width=15
        )
        self.start_dropdown.pack(pady=5)
        self.start_dropdown.set("Select")

        # END STOP
        end_box = tk.Frame(top_row, bg="white", bd=2, relief="solid")
        end_box.grid(row=0, column=1, padx=20, ipadx=20, ipady=10)

        tk.Label(end_box, text="End Stop", font=("Arial", 14), bg="white").pack()

        self.end_var = tk.StringVar()
        self.end_dropdown = ttk.Combobox(
            end_box,
            textvariable=self.end_var,
            values=stops_list,
            state="readonly",
            width=15
        )
        self.end_dropdown.pack(pady=5)
        self.end_dropdown.set("Select")

        # TIMING
        time_box = tk.Frame(left_frame, bg="white", bd=2, relief="solid")
        time_box.pack(pady=20, ipadx=20, ipady=10)

        tk.Label(time_box, text="Time (24-hour format)", bg="white", font=("Arial", 12)).pack(pady=5)

        time_frame = tk.Frame(time_box, bg="white")
        time_frame.pack()

        self.hour_var = tk.StringVar(value="00")
        tk.Spinbox(time_frame, from_=0, to=23, wrap=True,
                   textvariable=self.hour_var, width=5, format="%02.0f").pack(side="left")

        tk.Label(time_frame, text=":", bg="white").pack(side="left")

        self.min_var = tk.StringVar(value="00")
        tk.Spinbox(time_frame, from_=0, to=59, wrap=True,
                   textvariable=self.min_var, width=5, format="%02.0f").pack(side="left")

        # SEARCH HISTORY BUTTON
        tk.Button(
            left_frame,
            text="Search History",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
            bd=2,
            relief="solid",
            padx=40,
            pady=15
        ).pack(pady=30)


o = login()