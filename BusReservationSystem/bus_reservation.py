import tkinter as tk
from tkinter import messagebox, PhotoImage
import sqlite3

conn = sqlite3.connect("bus_reservation.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, name TEXT, bus TEXT, seat TEXT)")
conn.commit()

buses = {"Bus 1": ["A1", "A2", "A3", "A4"], "Bus 2": ["B1", "B2", "B3", "B4"]}
get_booked = lambda b: [s[0] for s in c.execute("SELECT seat FROM bookings WHERE LOWER(bus)=?", (b.lower(),))]

def clear(): [w.destroy() for w in root.winfo_children()]; root.image_store = []
def btn(txt, cmd, img=None, bg="#3399ff"): 
    try: ic = PhotoImage(file=img); root.image_store.append(ic)
    except: ic = None
    tk.Button(root, text=f"  {txt}" if ic else txt, image=ic, compound="left", font=("Arial",14),
              bg=bg, fg="white", padx=10, pady=5, command=cmd).pack(pady=5)

def main_menu():
    clear(); tk.Label(root, text="🚌 Bus Reservation System", font=("Arial", 24, "bold"), bg="#003366", fg="white").pack(pady=30)
    for t, f, i in [("Book Ticket", book_ui, "book_icon.png"), ("Search Booking", search_ui, "search_icon.png"),
                    ("Cancel Booking", cancel_ui, "cancel_icon.png"), ("View All Bookings", view_all, "view_icon.png")]: btn(t, f, i)
    btn("Exit", root.quit, bg="red")

def book_ui():
    clear(); tk.Label(root, text="🎟 Book Ticket", font=("Arial", 20, "bold"), bg="#0066cc", fg="white").pack(fill="x", pady=20)
    f = tk.Frame(root, bg="#e6f0ff"); f.pack(pady=20)
    name, bus, seat = tk.StringVar(), tk.StringVar(value="Bus 1"), tk.StringVar()
    tk.Label(f, text="Name", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(f, textvariable=name, font=("Arial", 14)).grid(row=0, column=1)
    tk.Label(f, text="Bus", font=("Arial", 14)).grid(row=1, column=0)
    tk.OptionMenu(f, bus, *buses).grid(row=1, column=1)
    tk.Label(f, text="Seat", font=("Arial", 14)).grid(row=2, column=0)
    seat_menu = tk.OptionMenu(f, seat, ""); seat_menu.grid(row=2, column=1)

    def update_seats(*_):
        s = [x for x in buses[bus.get()] if x not in get_booked(bus.get())]
        seat.set(s[0] if s else "No seats")
        seat_menu["menu"].delete(0, "end")
        [seat_menu["menu"].add_command(label=i, command=tk._setit(seat, i)) for i in s]
    bus.trace("w", update_seats); update_seats()

    def confirm():
        n, b, s = name.get().strip(), bus.get(), seat.get()
        if not n or s == "No seats": return messagebox.showerror("Error", "Enter valid name and seat.")
        if c.execute("SELECT * FROM bookings WHERE LOWER(name)=? AND LOWER(bus)=?", (n.lower(), b.lower())).fetchone():
            return messagebox.showerror("Error", "Already booked.")
        c.execute("INSERT INTO bookings (name, bus, seat) VALUES (?, ?, ?)", (n, b, s)); conn.commit()
        messagebox.showinfo("Success", f"Booked: {n}, {b}, seat {s}"); main_menu()

    [btn(t, a, bg=c) for t, a, c in [("Book", confirm, "#3399ff"), ("Back", main_menu, "black")]]

def search_ui():
    clear(); tk.Label(root, text="🔍 Search Booking", font=("Arial", 20, "bold"), bg="#0066cc", fg="white").pack(fill="x", pady=20)
    tk.Label(root, text="Enter Name or Bus", font=("Arial", 14)).pack(pady=10)
    e = tk.Entry(root, font=("Arial", 14)); e.pack()
    def search():
        val = e.get().strip().lower()
        res = c.execute("SELECT * FROM bookings WHERE LOWER(name)=? OR LOWER(bus)=?", (val, val)).fetchall()
        m = "\n".join([f"ID:{r[0]} | Name:{r[1]} | Bus:{r[2]} | Seat:{r[3]}" for r in res]) if res else "No booking found."
        messagebox.showinfo("Results", m)
    [btn(t, f, bg=b) for t, f, b in [("Search", search, "#3399ff"), ("Back", main_menu, "black")]]

def cancel_ui():
    clear(); tk.Label(root, text="❌ Cancel Booking", font=("Arial", 20, "bold"), bg="#cc0000", fg="white").pack(fill="x", pady=20)
    tk.Label(root, text="Enter Name and Bus", font=("Arial", 14)).pack(pady=10)
    n, b = tk.Entry(root, font=("Arial", 14)), tk.Entry(root, font=("Arial", 14))
    n.pack(); b.pack()
    def cancel():
        name, bus = n.get().strip().lower(), b.get().strip().lower()
        row = c.execute("SELECT * FROM bookings WHERE LOWER(name)=? AND LOWER(bus)=?", (name, bus)).fetchone()
        if row: c.execute("DELETE FROM bookings WHERE id=?", (row[0],)); conn.commit(); messagebox.showinfo("Cancelled", "Booking cancelled.")
        else: messagebox.showinfo("Not Found", "No booking found.")
    [btn(t, f, bg=c) for t, f, c in [("Cancel Booking", cancel, "#ff5050"), ("Back", main_menu, "black")]]

def view_all():
    clear(); tk.Label(root, text="📋 All Bookings", font=("Arial", 20, "bold"), bg="#0066cc", fg="white").pack(fill="x", pady=20)
    rows = c.execute("SELECT * FROM bookings").fetchall()
    [tk.Label(root, text=f"ID:{r[0]} | Name:{r[1]} | Bus:{r[2]} | Seat:{r[3]}", font=("Arial", 12)).pack() for r in rows] if rows \
        else tk.Label(root, text="No bookings found.", font=("Arial", 12)).pack()
    btn("Back", main_menu, bg="black")

# ======== START ========
root = tk.Tk(); root.title("Bus Reservation System")
root.state("zoomed"); root.configure(bg="#f0f8ff"); root.image_store = []
main_menu(); root.mainloop()