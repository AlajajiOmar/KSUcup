import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import TicketingDB
import sqlite3


class Student_window:
    def __init__(self, id):
        self.sid = id
        self.window = tk.Tk()
        self.window.title("Student window")
        self.window.geometry('600x500')
        self.window.configure(background='light blue')
        self.notebook = ttk.Notebook(self.window, width=600, height=500)
        self.notebook.pack(pady=10, expand=True)

        self.label_frame1 = tk.Frame(self.window, background='light blue', width=600, height=500)
        self.frame1 = tk.Frame(self.label_frame1, width=600, height=500, bg="light blue")
        self.label_frame2 = tk.Frame(self.window, background='light blue')
        self.frame2 = tk.Frame(self.label_frame2)

        # tuple
        event_tuble = TicketingDB.activeEvent()
        Select_tuple = tk.StringVar()
        self.pri = ttk.Combobox(self.frame1, textvariable=Select_tuple, width=60)
        self.pri['values'] = event_tuble
        self.pri.current()

        # page1

        # Buttons
        self.book_button = tk.Button(self.frame1, text=" Book ", width=10, height=1, command=self.Book_button)
        self.log_out = tk.Button(self.frame1, text="Log out", width=10, height=1, command=self.logout)
        # labels
        self.top_label = tk.Label(self.frame1, text="Active sport Events", width=100, height=15, bg="light blue")
        ##packs for page 1
        self.label_frame1.pack()
        self.frame1.pack()
        self.top_label.pack()
        self.pri.pack()
        self.book_button.pack(padx=10, pady=10)
        self.log_out.pack(padx=10, pady=10)

        # page2
        self.tv = ttk.Treeview(self.label_frame2, columns=(1, 2, 3), show='headings', height=10)

        # buttons
        self.show = tk.Button(self.label_frame2, text="Show Booking", width=10, height=1, command=self.showb)
        self.log_out2 = tk.Button(self.label_frame2, text="Log out", width=10, height=1, command=self.logout)

        # packs
        self.label_frame2.pack()
        self.show.pack(pady=10, padx=5)
        self.log_out2.pack(pady=10, padx=5)
        self.tv.pack()
        # notebook
        self.notebook.add(self.label_frame1, text="Book a Ticket")
        self.notebook.add(self.label_frame2, text="View my tickets")

        self.window.mainloop()

    # def
    def logout(self):
        self.window.destroy()
        from SignUp import signUp
        signUp()

    def Book_button(self):
        s = self.pri.get()
        lista = s.split(" ")[1]
        event_id = lista[0:len(lista)-1]
        a = TicketingDB.book(self.sid, event_id)
        if a == 'Sorry event is fully booked':
            messagebox.showerror("FULL", a)
        elif a == 'already booked':
            messagebox.showerror("CAN'T BOOK", a)
        else:
            messagebox.showinfo("DONE", a)
            namea = s.split(" ")[3]
            name = namea[0:len(namea) - 1]

            loca = s.split(" ")[5]
            loc = loca[0:len(loca) - 1]

            self.loggIt(name, loc)

    def loggIt(self, name, location):
        import logging
        logging.basicConfig(filename='transactions.log',
                            filemode='a',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info(f"The sport name: {name} in location: {location}, was booked by Student ID: {self.sid}")
    def showb(self):
        self.tv.destroy()
        self.tv = ttk.Treeview(self.label_frame2, columns=(1, 2, 3), show='headings', height=10)
        self.tv.heading(1, text="Name")
        self.tv.heading(2, text="Location")
        self.tv.heading(3, text="Date & time")

        self.cursor = TicketingDB.activeBokings(self.sid)
        count = 0
        for row in self.cursor:
            self.tv.insert(parent='', index=count, text='', values=(row[0], row[1], row[2]))
            count += 1
        self.tv.pack()


