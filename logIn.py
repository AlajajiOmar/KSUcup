import tkinter as tk
from tkinter import ttk, messagebox
class LogIn:
    def __init__(self):
        self.page = tk.Tk()
        self.page.geometry('600x400')
        self.page.title("Log in ")
        self.page.configure(background='light blue')
        self.frame = tk.Frame(self.page, background='light blue')
        self.bframe = tk.Frame(self.page, background='light blue')
        self.rframe = tk.Frame(self.frame, background='light blue')
        self.lframe = tk.Frame(self.frame, background='light blue')

        self.id = tk.Label( self.lframe, text='ID :', background='light blue')
        self.eid = tk.Entry(self.rframe, borderwidth=0)
        self.password = tk.Label( self.lframe, text='password :', background='light blue')
        self.epassword = tk.Entry(self.rframe, borderwidth=0)

        self.login = tk.Button(self.bframe,command=self.submit, text="Login", borderwidth=0, height=1, width=10, highlightcolor='gray')


        self.frame.pack()
        self.lframe.pack(side='left')
        self.rframe.pack(side='right', padx=15)
        self.bframe.pack(pady=40)

        self.id.pack(pady=10)
        self.eid.pack(pady=10)
        self.password.pack(pady=10)
        self.epassword.pack(pady=10)
        self.login.pack()

        self.page.mainloop()

    def valdite(self):
         if  self.eid.get() == ''  or self.epassword.get() == '' :
             tk.messagebox.showinfo('Results', 'please enter all the information')
             return False
         import re
         x=''
         reg = "^[0-9]{10}$"
         n = re.search(reg, self.eid.get())
         if not (n):
             x += '- ID should be 10 digits \n'
         if not (self.epassword.get().isalnum()) or len(self.epassword.get()) < 6:
                 x += 'Password contains at least 6 digits or numbers \n'
         if x !='':
            tk.messagebox.showinfo('Results', x)
            return False
         return True


    def submit(self):
        if not(self.valdite()):
            return
        import TicketingDB
        import hashlib
        t = self.eid.get()
        a=TicketingDB.loginS(self.eid.get(), hashlib.sha256(self.epassword.get().encode()).hexdigest())
        if a =='account does not exist' or a=='Wrong password':
            tk.messagebox.showinfo('Results', a)
        elif a=='admin':
            self.page.destroy()
            from Admin import Admin
            Admin(t)
        else :
            self.page.destroy()
            from student_window import Student_window
            Student_window(t)









