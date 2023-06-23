import tkinter as tk
from tkinter import ttk, messagebox

class signUp:
    def __init__(self):
        self.page = tk.Tk()
        self.page.geometry('600x400')
        self.page.title("Sign up ")
        self.page.configure(background='light blue')

        self.frame =tk.Frame(self.page ,background='light blue')
        self.bframe = tk.Frame(self.page ,background='light blue')
        self.rframe = tk.Frame(self.frame,background='light blue')
        self.lframe = tk.Frame(self.frame,background='light blue')

        self.name = tk.Label(self.lframe , text='Name :' ,background='light blue')
        self.ename = tk.Entry(self.rframe, borderwidth=0)
        self.id = tk.Label(self.lframe, text='ID :',background='light blue')
        self.eid = tk.Entry(self.rframe, borderwidth=0)
        self.password = tk.Label(self.lframe, text='password :',background='light blue')
        self.epassword = tk.Entry(self.rframe, borderwidth=0)
        self.email = tk.Label(self.lframe, text='Email :',background='light blue')
        self.eemail= tk.Entry(self.rframe, borderwidth=0)
        self.phone = tk.Label(self.lframe, text='Phone number :',background='light blue')
        self.ephone = tk.Entry(self.rframe, borderwidth=0)


        self.sub = tk.Button(self.bframe ,text="Submit" ,command=self.submit, borderwidth=0 ,height=1 , width=10 ,highlightcolor='gray')
        self.login = tk.Button(self.bframe,text="Login",command=self.loginpushed, borderwidth=0,height=1 , width=10 ,highlightcolor='gray')

        self.frame.pack()
        self.lframe.pack(side='left')
        self.rframe.pack(side='right' , padx=15)
        self.bframe.pack(pady=40)
        self.name.pack(pady=10)
        self.ename.pack(pady=10)
        self.id.pack(pady=10)
        self.eid.pack(pady=10)
        self.password.pack(pady=10)
        self.epassword.pack(pady=10)
        self.email.pack(pady=10)
        self.eemail.pack(pady=10)
        self.phone.pack(pady=10)
        self.ephone.pack(pady=10)
        self.sub.pack(side="left",padx=30)
        self.login.pack(padx=30)


        self.page.mainloop()
    def loginpushed(self):
        self.page.destroy()
        from logIn import LogIn
        LogIn()

    def valdite(self):
        if self.ename.get() == '' or self.eid.get() == '' or self.ephone.get() == '' or self.epassword.get() == '' or self.eemail.get() == '':
            tk.messagebox.showinfo('Results', 'please enter all the information')
            return False
        import re
        x =''
        reg = "^[a-zA-Z]+ [a-zA-Z]+$"
        n = re.search(reg,self.ename.get())
        if not(n):
            x += '- names should Consist of first and last names and they made of characters\n'
        reg = "^[0-9]{10}$"
        n = re.search(reg, self.eid.get())
        if not (n):
            x += '- ID should be 10 digits\n'
        if not(self.epassword.get().isalnum()) or len(self.epassword.get())<6 :
             x+='- Password contains at least 6 digits or letters\n'

        reg = "^([a-zA-Z0-9\._-]+)@(student.|)(ksu.edu.sa)$"
        n = re.search(reg, self.eemail.get())
        if not(n):
            x += '- Email should be a valid ksu email\n'
        reg = "^(05)[0-9]{8}$"
        n = re.search(reg, self.ephone.get())
        if not(n):
            x += '- Phone numbers should start with 05 and have 10 digits \n'
        if x !='':
            tk.messagebox.showinfo('Results', x)
            return False
        return True
    def submit(self):
        if not(self.valdite()):
            return
        import TicketingDB
        import hashlib
        a=TicketingDB.createSAccount(self.eid.get(), self.ename.get(), hashlib.sha256(self.epassword.get().encode()).hexdigest()
                           , self.ephone.get(), self.eemail.get())
        if a:
            tk.messagebox.showinfo('Results', 'Account has been created successfully please press log in to proceed')
        else:
            tk.messagebox.showinfo('Results', 'Account already exists please press log in to proceed')




















gui = signUp()



