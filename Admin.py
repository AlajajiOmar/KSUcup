import sqlite3
import tkinter as tk
import tkinter.messagebox
import random
import tkcalendar
from tktimepicker import AnalogPicker, AnalogThemes
from datetime import datetime
import TicketingDB
'''
Before starting installing these packages is important all of them are made in tkinter
pip install tkinter
pip install tkcalendar
pip install tktimepicker
pip install sqlite3
pip install random
'''


class Admin:
    def __init__(self, aid):
        self.aid = aid
        self.window = tk.Tk()
        self.window.title("Admin")
        self.window.geometry('280x240')
        self.window.configure(bg='light blue')
        self.window.eval('tk::PlaceWindow . center')  # to make screen start in the middle of the screen
        self.labelFrame = tk.LabelFrame(self.window, text='Admin ', bg='light blue')
        self.labelFrame.pack(fill="both", expand='yes', padx=10, pady=10)
        self.labelFrame.configure(font=("Helvetica 14 bold"))

        # Buttons
        self.button_create = tk.Button(self.labelFrame, text='Create', width=35, command=self.create)
        self.button_back_up = tk.Button(self.labelFrame, text='Backup', width=35, command=self.backup)
        self.button_log_out = tk.Button(self.labelFrame, text='Logout', command=self.logout, width=15)
        self.button_event_time = tk.Button(self.labelFrame, text='Select time', width=21, command=self.selectTime)
        # Labels
        self.label_event_name = tk.Label(self.labelFrame, text="Event Name: ", bg="light blue")
        self.label_event_location = tk.Label(self.labelFrame, text="Event Location: ", bg="light blue")
        self.label_event_capacity = tk.Label(self.labelFrame, text="Event Capacity: ", bg="light blue")
        self.label_event_date = tk.Label(self.labelFrame, text="Event date: ", bg="light blue")
        self.label_event_time = tk.Label(self.labelFrame, text="Event time: ", bg="light blue")
        # Entries
        self.entry_event_name = tk.Entry(self.labelFrame, text="", width=25)
        self.entry_event_location = tk.Entry(self.labelFrame, text="", width=25)
        self.entry_event_capacity = tk.Entry(self.labelFrame, text="", width=25)
        self.entry_event_date = tkcalendar.DateEntry(self.labelFrame, selectmode='day', width=22)

        self.default_date = self.entry_event_date.get()
        # Packing labels
        self.label_event_name.grid(column=0, row=0)
        self.entry_event_name.grid(column=1, row=0)

        self.label_event_location.grid(column=0, row=1)
        self.entry_event_location.grid(column=1, row=1)

        self.label_event_capacity.grid(column=0, row=2)
        self.entry_event_capacity.grid(column=1, row=2)

        self.label_event_date.grid(column=0, row=3)
        self.entry_event_date.grid(column=1, row=3)

        self.label_event_time.grid(column=0, row=4)
        self.button_event_time.grid(column=1, row=4)

        self.button_create.grid(column=0, row=5, columnspan=2, pady=1)
        self.button_back_up.grid(column=0, row=6, columnspan=2, pady=1)
        self.button_log_out.grid(column=0, row=7, columnspan=2, pady=1)

        # Data to validate
        self.error_list = list()
        self.information = dict()
        self.hours = None
        self.minutes = None
        self.period = None
        self.time_window = None
        self.time_picker = None
        self.theme = None
        self.entry_event_name.focus()
        self.window.mainloop()

    def clear(self):

        self.error_list = list()
        self.entry_event_name.delete(0, tk.END)
        self.entry_event_location.delete(0, tk.END)
        self.entry_event_capacity.delete(0, tk.END)
        self.entry_event_date.delete(0, tk.END)
        self.hours = None
        self.minutes = None
        self.period = None
        self.time_window = None
        self.time_picker = None
        self.theme = None
        self.entry_event_name.focus()

    def is_empty(self):
        try:
            self.information['name'] = self.entry_event_name.get()
            self.information['location'] = self.entry_event_location.get()
            self.information['capacity'] = self.entry_event_capacity.get()
            self.information['time'] = self.entry_event_date.get()
            datetime_str = self.information['time'] + " " + str(self.hours) + ":" + str(self.minutes) + " " + str(
                self.period)
            self.information['time'] = datetime.strptime(datetime_str, "%m/%d/%y %I:%M %p").strftime("%Y-%m-%d %I:%M %p")

            for i in self.information:
                if self.information[i] == "":
                    tkinter.messagebox.showerror("Empty fields", "Please fill the fields")
                    return False
            return True
        except:
            tkinter.messagebox.showerror("Something Wrong", "Please check all fields especially the date and time "
                                                            "and please stick with the format")
            return False

    def numOfDays(self, d2):
        t = datetime.today()
        s = self.information['time'].split(" ")
        x = datetime.strptime(s[0], "%Y-%m-%d")

        return x > datetime.strptime(t.strftime("%Y-%m-%d"), "%Y-%m-%d")

    def checkFields(self):
        if not self.information['name'].isalnum():
            self.error_list.append("Event name need to be alphanumeric")

        if not self.information['location'].isalnum():
            self.error_list.append("Event Location need to be alphanumeric")

        if not self.information['capacity'].isdigit():
            self.error_list.append("Event Capacity need to be digits and not negative")
        if not self.numOfDays(self.information["time"]):
            self.error_list.append("Event Date need to in the present")
        if len(self.error_list) == 0:
            return True
        else:
            return False

    def create(self):
        if not self.is_empty():
            return
        if not self.checkFields():
            t = ""
            for i in self.error_list:
                t += "- " + i + "\n"
            tkinter.messagebox.showerror("Field Error", t)
            self.error_list = list()
            t = ""
            return

        self.writeDB()
        self.clear()

    def writeDB(self):
        id = self.generateID()
        flag = True
        while flag:
            if TicketingDB.checkExist(id):
                flag = False
            else:
                id = self.generateID()
        TicketingDB.writeEvent(id, self.information['name'], self.information['location'], self.information['capacity'],
                               self.information['time'], self.aid, '0')
        pass

    def generateID(self):
        x = random.sample(range(0, 9), 5)
        t = ""
        for i in x:
            t += str(i)
        return t

    def backup(self):
        TicketingDB.backUP()

    def selectTime(self):
        self.time_window = tk.Tk()
        self.time_window.eval('tk::PlaceWindow . center')
        self.time_window.title("Selecting Time")
        self.time_picker = AnalogPicker(self.time_window)
        self.theme = AnalogThemes(self.time_picker)
        self.theme.setNavyBlue()
        self.time_picker.pack(expand=True, fill="both")
        self.time_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.time_window.mainloop()

    def on_closing(self):
        self.setTime()
        self.time_window.destroy()

    def setTime(self):
        self.hours, self.minutes, self.period = self.time_picker.time()

    def logout(self):
        self.window.destroy()
        from SignUp import signUp
        signUp()

