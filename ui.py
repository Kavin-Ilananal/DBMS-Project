import oracledb
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
from db_queries import get_available_buses, get_routes_with_transfers
from dotenv import load_dotenv
import os
import json

load_dotenv()


class login:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.configure(bg="#1e1e2f")
        self.login_window.geometry("1400x800")
        self.login_window.title("Login credentials")

        l_frame = tk.Frame(self.login_window, bg="#1e1e2f")
        l_frame.pack(pady=40)

        tk.Label(
            l_frame, text="Username", bg="#1e1e2f", fg="white", font=("Arial", 12)
        ).grid(row=0, column=0, pady=10, sticky="w")

        self.username_entry = tk.Entry(
            l_frame, font=("Arial", 12), fg="white",
            bg="#2c2c3e", insertbackground="white"
        )
        self.username_entry.grid(row=0, column=1, pady=10)

        tk.Label(
            l_frame, text="Password", bg="#1e1e2f", fg="white", font=("Arial", 12)
        ).grid(row=1, column=0, pady=10)

        self.password_entry = tk.Entry(
            l_frame, show="*", font=("Arial", 12),
            fg="white", bg="#2c2c3e", insertbackground="white"
        )
        self.password_entry.grid(row=1, column=1, pady=10)

        tk.Button(
            self.login_window, text='Login', command=self.login
        ).pack(pady=20)
        tk.Button(
			self.login_window,
			text="Sign Up",
			command=self.open_signup,
			bg="#1976d2",
			fg="white"
		).pack(pady=10)

        self.login_window.mainloop()

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
                SELECT user_id FROM users 
                WHERE name = :1 AND password = :2
            """, (username, password))

            user = cursor.fetchone()

            if user:
                self.current_user_id = user[0]   # ⭐ VERY IMPORTANT
                self.show_main_screen()
            else:
                messagebox.showerror("Login Failed", "Invalid Username or password")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_signup(self):
        signup = tk.Toplevel(self.login_window)
        signup.title("Sign Up")
        signup.geometry("400x400")
        signup.configure(bg="#1e1e2f")

        frame = tk.Frame(signup, bg="#1e1e2f")
        frame.pack(pady=20)

        # NAME
        tk.Label(frame, text="Name", bg="#1e1e2f", fg="white").grid(row=0, column=0, pady=10)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=0, column=1)

        # PHONE
        tk.Label(frame, text="Phone", bg="#1e1e2f", fg="white").grid(row=1, column=0, pady=10)
        phone_entry = tk.Entry(frame)
        phone_entry.grid(row=1, column=1)

        # EMAIL
        tk.Label(frame, text="Email", bg="#1e1e2f", fg="white").grid(row=2, column=0, pady=10)
        email_entry = tk.Entry(frame)
        email_entry.grid(row=2, column=1)

        # PASSWORD
        tk.Label(frame, text="Password", bg="#1e1e2f", fg="white").grid(row=3, column=0, pady=10)
        password_entry = tk.Entry(frame, show="*")
        password_entry.grid(row=3, column=1)

        # SIGNUP BUTTON
        tk.Button(
            signup,
            text="Register",
            command=lambda: self.register_user(
            name_entry.get(),
            phone_entry.get(),
            email_entry.get(),
            password_entry.get(),
            signup
            ),
            bg="#1976d2",
            fg="white"
        ).pack(pady=20)

    def register_user(self, name, phone, email, password, window):
        try:
            conn = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=os.getenv("DB_DSN")
            )
            cursor = conn.cursor()

            # GENERATE USER ID
            cursor.execute("SELECT NVL(MAX(user_id),0)+1 FROM users")
            user_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO users (user_id, name, phone_no, email, password)
                VALUES (:1, :2, :3, :4, :5)
            """, (user_id, name, phone, email, password))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "User Registered Successfully")
            window.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_main_screen(self):
        for widget in self.login_window.winfo_children():
            widget.destroy()

        self.login_window.configure(bg="#eaeaea")

        main_frame = tk.Frame(self.login_window, bg="#eaeaea")
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#eaeaea")
        left_frame.pack(side="left", anchor="nw", padx=20, pady=20)

        stops_list = self.get_stops()

        # TOP ROW
        top_row = tk.Frame(left_frame, bg="#eaeaea")
        top_row.pack(pady=20)

        # START STOP
        start_box = tk.Frame(top_row, bg="white", bd=2, relief="solid")
        start_box.grid(row=0, column=0, padx=20, ipadx=20, ipady=10)

        tk.Label(start_box, text="Start Stop", font=("Arial", 14), bg="white").pack()

        self.start_var = tk.StringVar()
        ttk.Combobox(
            start_box,
            textvariable=self.start_var,
            values=stops_list,
            state="readonly",
            width=15
        ).pack(pady=5)

        self.start_var.set("Select")

        # END STOP
        end_box = tk.Frame(top_row, bg="white", bd=2, relief="solid")
        end_box.grid(row=0, column=1, padx=20, ipadx=20, ipady=10)

        tk.Label(end_box, text="End Stop", font=("Arial", 14), bg="white").pack()

        self.end_var = tk.StringVar()
        ttk.Combobox(
            end_box,
            textvariable=self.end_var,
            values=stops_list,
            state="readonly",
            width=15
        ).pack(pady=5)

        self.end_var.set("Select")

        # TIME
        time_box = tk.Frame(left_frame, bg="white", bd=2, relief="solid")
        time_box.pack(pady=20, ipadx=20, ipady=10)

        # DATE
        date_box = tk.Frame(left_frame, bg="white", bd=2, relief="solid")
        date_box.pack(pady=10, ipadx=20, ipady=10)

        tk.Label(date_box, text="Date", bg="white", font=("Arial", 12)).pack()

        self.date_entry = DateEntry(
            date_box,
            date_pattern="yyyy-mm-dd",
            background="#1976d2",
            foreground="white",
            borderwidth=2
            )
        self.date_entry.pack(pady=5)

        tk.Label(time_box, text="Time", bg="white", font=("Arial", 12)).pack()

        time_frame = tk.Frame(time_box, bg="white")
        time_frame.pack()

        self.hour_var = tk.StringVar(value="00")
        tk.Spinbox(time_frame, from_=0, to=23, wrap=True,
                   textvariable=self.hour_var, width=5, format="%02.0f").pack(side="left")

        tk.Label(time_frame, text=":", bg="white").pack(side="left")

        self.min_var = tk.StringVar(value="00")
        tk.Spinbox(time_frame, from_=0, to=59, wrap=True,
                   textvariable=self.min_var, width=5, format="%02.0f").pack(side="left")

        # CHECK BUTTON
        tk.Button(
            left_frame,
            text="Check",
            font=("Arial", 14, "bold"),
            bg="white",
            command=self.check_availability
        ).pack(pady=10)

        # SEARCH HISTORY BUTTON
        tk.Button(
            left_frame,
            text="Search History",
            font=("Arial", 14, "bold"),
            bg="white",
            bd=2,
            relief="solid",
            padx=40,
            pady=15,
            command=self.show_history_popup   # ⭐ ADD THIS
        ).pack(pady=30)
        self.right_frame = tk.Frame(main_frame, bg="#bbdefb")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            self.right_frame,
            text="Available Buses",
            font=("Arial", 16, "bold"),
            fg="#0d47a1",
            bg="#bbdefb"
        ).pack(anchor="nw")

    def check_availability(self):
        try:
            start = self.start_var.get()
            end = self.end_var.get()
            time = f"{self.hour_var.get()}:{self.min_var.get()}"
            selected_date = self.date_entry.get()
            date_obj = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
            day = date_obj.strftime("%A")

            # CONNECT TO DB TO GET stop_ids
            conn = oracledb.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dsn=os.getenv("DB_DSN")
            )
            cursor = conn.cursor()

            cursor.execute("SELECT stop_id FROM stops WHERE stop_name = :1", (start,))
            row = cursor.fetchone()

            if not row:
                messagebox.showerror("Error", "Invalid start stop")
                return

            start_id = row[0]

            cursor.execute("SELECT stop_id FROM stops WHERE stop_name = :1", (end,))
            row = cursor.fetchone()

            if not row:
                messagebox.showerror("Error", "Invalid end stop")
                return

            end_id = row[0]
            conn.close()

            # CALL QUERY FUNCTION
            if start == "Select" or end == "Select":
                messagebox.showerror("Error", "Please select stops")
                return

            direct_results = get_available_buses(start_id, end_id, time, day)
            transfer_results = get_routes_with_transfers(start_id, end_id, time, day)

            direct_results = direct_results[:4]       # top 4
            transfer_results = transfer_results[:2]   # top 2
            
            

            # CLEAR RIGHT PANEL
            for widget in self.right_frame.winfo_children():
                widget.destroy()

            tk.Label(
                self.right_frame,
                text="Available Buses".upper(),
                font=("Arial", 20, "bold"),
                bg="#bbdefb"
            ).pack(anchor="nw")

            # DISPLAY EACH ROUTE
            if not direct_results:
                tk.Label(
                self.right_frame,
                text="No direct buses available",
                font=("Arial", 14),
                bg="white"
                ).pack(pady=20)

            tk.Label(
                self.right_frame,
                text="Direct Buses",
                font=("Arial", 16, "bold"),
                bg="#bbdefb"
            ).pack(anchor="w", padx=10, pady=5)

            for row in direct_results:
                (
                route_id,
                bus_id,
                name,
                phone,
                photo,
                license_no,
                exp,
                bus_type,
                get_on_time,
                get_off_time,
                fare
                ) = row

                box = tk.Frame(self.right_frame, bg="#e3f2fd", bd=2, relief="solid")
                box.pack(fill="x", padx=10, pady=10)

                tk.Label(
                    box,
                    text=f"Bus: {bus_id} | {get_on_time} → {get_off_time} | ₹{fare}",
                    font=("Arial", 12, "bold"),
                    bg="#e3f2fd"
                ).pack(anchor="w", padx=10, pady=5)

                tk.Button(
                    box,
                    text="View Details",
                    command=lambda r=row: self.show_details(r)
                ).pack(anchor="e", padx=10, pady=5)
            # -------------------------------
            # TRANSFER ROUTES HEADER
            # -------------------------------
            tk.Label(
                self.right_frame,
                text="Transfer Routes",
                font=("Arial", 16, "bold"),
                bg="#bbdefb"
            ).pack(anchor="w", padx=10, pady=10)

            if not transfer_results:
                tk.Label(
                    self.right_frame,
                    text="No transfer routes",
                    bg="#bbdefb"
                ).pack()

            # -------------------------------
            # DISPLAY TRANSFER ROUTES
            # -------------------------------
            for row in transfer_results:
                (
                    r1, b1, d1, p1,ph1, l1, e1,
                    t1, transfer_stop, t2,
                    r2, b2, d2, p2,ph2, l2, e2,
                    t3, t4, total_fare
                ) = row

                box = tk.Frame(self.right_frame, bg="#fff3e0", bd=2, relief="solid")
                box.pack(fill="x", padx=10, pady=10)

                tk.Label(
                   box,
                   text=f"Bus {b1} → {transfer_stop} → Bus {b2}",
                   font=("Arial", 12, "bold"),
                   bg="#fff3e0"
                ).pack(anchor="w", padx=10, pady=5)

                tk.Label(
                    box,
                    text=f"{t1} → {t2} | {t3} → {t4} | ₹{total_fare}",
                    bg="#fff3e0"
                ).pack(anchor="w", padx=10)

                tk.Button(
                    box,
                    text="View Details",
                    command=lambda r=row: self.show_transfer_details(r)
                ).pack(anchor="e", padx=10, pady=5)
            history_entry = {
                    "start": start,
                    "end": end,
                    "time": time,
                    "date": selected_date,
                    "day": day,

                    "direct": [
                        {
                            "route_id": r[0],
                            "bus_id": r[1],
                            "driver": r[2],
                            "phone": r[3],
                            "license": r[5],
                            "experience": r[6],
                            "bus_type": r[7],
                            "get_on": r[8],
                            "get_off": r[9],
                            "fare": r[10]
                        }
                        for r in direct_results
                    ],

                    "transfer": [
                        {
                            "route1": r[0],
                            "bus1": r[1],
                            "driver1": r[2],
                            "phone1": r[3],
                            "license1": r[5],
                            "experience1": r[6],
                            "board_time1": r[7],
                            "drop_time1": r[8],
                            "transfer_stop": r[9],

                            "route2": r[10],
                            "bus2": r[11],
                            "driver2": r[12],
                            "phone2": r[13],
                            "license2": r[15],
                            "experience2": r[16],
                            "board_time2": r[17],
                            "drop_time2": r[18],

                            "total_fare": r[19]
                        }
                        for r in transfer_results
                    ]
            }

            snapshot = json.dumps(history_entry)
            self.save_search_to_db(start_id, end_id, time, day, snapshot)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_top_history(self):
        conn = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=os.getenv("DB_DSN")
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT result_snapshot, searched_at
            FROM search_history
            WHERE user_id = :user_id
            ORDER BY searched_at DESC
            FETCH FIRST 5 ROWS ONLY
        """, {"user_id": self.current_user_id})

        rows = cursor.fetchall()
        conn.close()

        return rows
    
    def show_history_popup(self):
        rows = self.get_top_history()

        popup = tk.Toplevel(self.login_window)
        popup.title("Recent Searches")
        popup.geometry("600x500")

        if not rows:
            tk.Label(popup, text="No History Found").pack()
            return

        for snapshot, timestamp in rows:
            data = json.loads(snapshot)

            box = tk.Frame(popup, bd=2, relief="solid")
            box.pack(fill="x", padx=10, pady=10)

            # TOP DISPLAY
            tk.Label(
                box,
                text=f"{data['start']} → {data['end']}",
                font=("Arial", 12, "bold")
            ).pack(anchor="w")

            tk.Label(
                box,
                text=f"{data['time']} | {data['day']} | {timestamp}",
            ).pack(anchor="w")

            # BUTTON
            tk.Button(
                box,
                text="View",
                command=lambda d=data, p=popup: self.load_history(d, p)
            ).pack(anchor="e", padx=10, pady=5)
    def load_history(self, data, popup):
        popup.destroy()   # close popup

        # clear right panel
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.right_frame,
            text="Available Buses",
            font=("Arial", 20, "bold"),
            bg="#bbdefb"
        ).pack(anchor="nw")

        # -------------------------
        # DIRECT BUSES
        # -------------------------
        tk.Label(
            self.right_frame,
            text="Direct Buses",
            font=("Arial", 16, "bold"),
            bg="#bbdefb"
        ).pack(anchor="w", padx=10, pady=5)

        for r in data["direct"]:
            box = tk.Frame(self.right_frame, bg="#e3f2fd", bd=2, relief="solid")
            box.pack(fill="x", padx=10, pady=10)

            tk.Label(
                box,
                text=f"Bus: {r['bus_id']} | {r['get_on']} → {r['get_off']} | ₹{r['fare']}",
                font=("Arial", 12, "bold"),
                bg="#e3f2fd"
            ).pack(anchor="w", padx=10, pady=5)

            # ⭐ ADD THIS BUTTON
            tk.Button(
                box,
                text="View Details",
                command=lambda r=r: self.show_details((
                    r['route_id'],
                    r['bus_id'],
                    r['driver'],
                    r['phone'],
                    "",  # photo placeholder
                    r['license'],
                    r['experience'],
                    r['bus_type'],
                    r['get_on'],
                    r['get_off'],
                    r['fare']
                ))
            ).pack(anchor="e", padx=10, pady=5)

        # -------------------------
        # TRANSFER ROUTES
        # -------------------------
        tk.Label(
            self.right_frame,
            text="Transfer Routes",
            font=("Arial", 16, "bold"),
            bg="#bbdefb"
        ).pack(anchor="w", padx=10, pady=10)

        for r in data["transfer"]:
            box = tk.Frame(self.right_frame, bg="#fff3e0", bd=2, relief="solid")
            box.pack(fill="x", padx=10, pady=10)

            tk.Label(
                box,
                text=f"Bus {r['bus1']} → {r['transfer_stop']} → Bus {r['bus2']}",
                font=("Arial", 12, "bold"),
                bg="#fff3e0"
            ).pack(anchor="w", padx=10)

            tk.Label(
                box,
                text=f"{r['board_time1']} → {r['drop_time1']} | {r['board_time2']} → {r['drop_time2']} | ₹{r['total_fare']}",
                bg="#fff3e0"
            ).pack(anchor="w", padx=10)

            # ⭐ ADD THIS BUTTON
            tk.Button(
                box,
                text="View Details",
                command=lambda r=r: self.show_transfer_details((
                    r['route1'], r['bus1'], r['driver1'], r['phone1'], "", r['license1'], r['experience1'],
                    r['board_time1'], r['transfer_stop'], r['drop_time1'],
                    r['route2'], r['bus2'], r['driver2'], r['phone2'], "", r['license2'], r['experience2'],
                    r['board_time2'], r['drop_time2'], r['total_fare']
                ))
            ).pack(anchor="e", padx=10, pady=5)

    def save_search_to_db(self, start_id, end_id, time, day, snapshot):
        try:
            conn = oracledb.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dsn=os.getenv("DB_DSN")
            )
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO search_history (
                    user_id,
                    from_stop_id,
                    to_stop_id,
                    time,
                    day,
                    result_snapshot
                )
                VALUES (:user_id, :start_id, :end_id, :time, :day, :snapshot)
            """, {
                "user_id": self.current_user_id,
                "start_id": start_id,
                "end_id": end_id,
                "time": time,
                "day": day,
                "snapshot": snapshot
            })
            print("day : ",day)
            conn.commit()
            conn.close()

        except Exception as e:
            print("DB History Error:", e)

    def show_details(self, row):
        popup = tk.Toplevel(self.login_window)
        popup.title("Bus Details")
        popup.geometry("400x400")
        popup.configure(bg="#e3f2fd")

        (
            route_id,
            bus_id,
            name,
            phone,
            photo,
            license_no,
            exp,
            bus_type,
            get_on_time,
            get_off_time,
            fare
        ) = row

        tk.Label(popup, text=f"Route: {route_id}", font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=10)
        tk.Label(popup, text=f"Bus ID: {bus_id}", bg="#e3f2fd").pack()
        tk.Label(popup, text=f"Driver: {name}", bg="#e3f2fd").pack()
        tk.Label(popup, text=f"Phone: {phone}", bg="#e3f2fd").pack()
        tk.Label(popup, text=f"License: {license_no}", bg="#e3f2fd").pack()
        tk.Label(popup, text=f"Experience: {exp} years", bg="#e3f2fd").pack()
        tk.Label(popup, text=f"Type: {bus_type}", bg="#e3f2fd").pack()

        tk.Label(
            popup,
            text=f"Time: {get_on_time} → {get_off_time}",
            font=("Arial", 12, "bold"),
            bg="#e3f2fd"
        ).pack(pady=10)

        tk.Label(
            popup,
            text=f"Fare: ₹{fare}",
            font=("Arial", 14, "bold"),
            fg="#d32f2f",
            bg="#e3f2fd"
        ).pack()

    def show_transfer_details(self, row):
        popup = tk.Toplevel(self.login_window)
        popup.title("Transfer Route Details")
        popup.geometry("500x600")
        popup.configure(bg="#fff3e0")

        (
                r1, b1, d1, p1,ph1, l1, e1,
                t1, transfer_stop, t2,
                r2, b2, d2, p2,ph2, l2, e2,
                t3, t4, total_fare
        ) = row

        tk.Label(popup, text="TRANSFER ROUTE", font=("Arial", 16, "bold"), bg="#fff3e0").pack(pady=10)

        # -------------------------
        # FIRST BUS DETAILS
        # -------------------------
        tk.Label(popup, text=f"Route: {r1}", font=("Arial", 12, "bold"), bg="#fff3e0").pack()
        tk.Label(popup, text=f"Bus ID: {b1}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"Driver: {d1}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"Phone: {p1}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"License: {l1}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"Experience: {e1} years", bg="#fff3e0").pack()

        tk.Label(
                popup,
                text=f"Time: {t1} → {t2}",
                font=("Arial", 12, "bold"),
                bg="#fff3e0"
        ).pack(pady=5)

        # -------------------------
        # TRANSFER POINT
        # -------------------------
        tk.Label(
                popup,
                text=f"Transfer at: {transfer_stop}",
                font=("Arial", 12, "bold"),
                bg="#fff3e0"
        ).pack(pady=10)

        # -------------------------
        # SECOND BUS DETAILS
        # -------------------------
        tk.Label(popup, text=f"Route: {r2}", font=("Arial", 12, "bold"), bg="#fff3e0").pack()
        tk.Label(popup, text=f"Bus ID: {b2}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"Driver: {d2}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"Phone: {p2}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"License: {l2}", bg="#fff3e0").pack()
        tk.Label(popup, text=f"Experience: {e2} years", bg="#fff3e0").pack()

        tk.Label(
                popup,
                text=f"Time: {t3} → {t4}",
                font=("Arial", 12, "bold"),
                bg="#fff3e0"
        ).pack(pady=5)

        # -------------------------
        # TOTAL FARE
        # -------------------------
        tk.Label(
                popup,
                text=f"Total Fare: ₹{total_fare}",
                font=("Arial", 14, "bold"),
                fg="#d32f2f",
                bg="#fff3e0"
        ).pack(pady=15)
o = login()