from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
import os

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("600x700")
        self.root.config(bg="white")

        # Creating Variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_passwd = StringVar()
        self.var_confPasswd = StringVar()

        # Title for Register Interface
        title = Label(self.root, text="REGISTER HERE", font=("Times New Roman", 30), bg="white",
                      fg="black").place(x=0, y=10, relwidth=1)

        # Contents in Register Page
        fname = Label(self.root, text="First Name", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=100)
        self.txt_fname = Entry(self.root, font=("times new roman", 15), bg="lightgray", textvariable=self.var_fname)
        self.txt_fname.place(x=50, y=130, width=250)

        lname = Label(self.root, text="Last Name", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=180)
        self.txt_lname = Entry(self.root, font=("times new roman", 15), bg="lightgray", textvariable=self.var_lname)
        self.txt_lname.place(x=50, y=210, width=250)

        contact = Label(self.root, text="Contact No.", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=260)
        self.txt_contact = Entry(self.root, font=("times new roman", 15), bg="lightgray", textvariable=self.var_contact)
        self.txt_contact.place(x=50, y=290, width=250)

        email = Label(self.root, text="Email", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=340)
        self.txt_email = Entry(self.root, font=("times new roman", 15), bg="lightgray", textvariable=self.var_email)
        self.txt_email.place(x=50, y=370, width=250)

        securityQ = Label(self.root, text="Security Question", font=("times new roman", 15, "bold"), bg="white").place(
            x=50, y=420)
        self.cmb_securityQ = ttk.Combobox(self.root, font=("times new roman", 13), state="readonly",
                                          justify=CENTER, textvariable=self.var_securityQ)
        self.cmb_securityQ['values'] = ("What was the city you were born in?", "What is your favorite movie?", "What was the name of your first pet?",
                                        "Who is your favorite author?", "What is the name of your best friend in high school?", "What is your favorite food?", "In what year did you graduate from high school?", "What is your mother's maiden name?", "What is the name of the street you grew up on?", "What is your favorite vacation destination?")
        self.cmb_securityQ.place(x=50, y=450, width=380)
        self.cmb_securityQ.current(0)

        securityA = Label(self.root, text="Security Answer", font=("times new roman", 15, "bold"), bg="white").place(
            x=50, y=500)
        self.txt_securityA = Entry(self.root, font=("times new roman", 15), bg="lightgray", textvariable=self.var_securityA)
        self.txt_securityA.place(x=50, y=530, width=250)

        passwd = Label(self.root, text="Password", font=("times new roman", 15, "bold"), bg="white").place(x=300, y=100)
        self.txt_passwd = Entry(self.root, font=("times new roman", 15), bg="lightgray", textvariable=self.var_passwd)
        self.txt_passwd.place(x=300, y=130, width=250)

        confPasswd = Label(self.root, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white").place(
            x=300, y=180)
        self.txt_confPasswd = Entry(self.root, font=("times new roman", 15), bg="lightgray",
                                    textvariable=self.var_confPasswd)
        self.txt_confPasswd.place(x=300, y=210, width=250)

        # Terms & Conditions Checkbox
        self.chk_var = IntVar()
        chk = Checkbutton(self.root, text="I Agree The Terms & Conditions", onvalue=1, offvalue=0, variable=self.chk_var,
                          font=("times new roman", 12, "bold"), bg="white")
        chk.place(x=300, y=260)

        UserType=Label(self.root, text="User", font=("times new roman", 15, "bold"), bg="white",fg="black").place(x=300,y=310)
        self.txt_UserType=ttk.Combobox (self.root, font=("times new roman",13), state="readonly",justify=CENTER)
        self.txt_UserType['values']=("Student")
        self.txt_UserType.place(x=300, y=350,width=120)
        self.txt_UserType.current (0)

        # Register Button
        self.btn_img = PhotoImage(file="register.png")
        btn = Button(self.root, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data).place(x=50, y=570)

        # Login Button
        self.btn_img_login = PhotoImage(file="login.png")
        btn_login = Button(self.root, image=self.btn_img_login, bd=0, cursor="hand2", command=self.login_window).place(
            x=250, y=570)

    def login_window(self):
        self.root.destroy()
        os.system("login.py")

    def register_data(self):
        if self.var_fname.get() == "" or self.var_lname.get() == "" or self.var_contact.get() == "" or self.var_email.get() == "" or \
                self.var_securityQ.get() == "Select" or self.var_securityA.get() == "" or self.var_passwd.get() == "" or \
                self.var_confPasswd.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)

        elif self.var_passwd.get() != self.var_confPasswd.get():
            messagebox.showerror("Error", "Password and Confirm Password should be the same", parent=self.root)

        elif self.chk_var.get() == 0:
            messagebox.showerror("Error", "Please Agree to the Terms & Conditions", parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="group1"
                )
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE email=%s", (self.var_email.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Email already registered, please try with a different email",
                                         parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO users (f_name, l_name, contact, email, securityQ, securityA, password, UserType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            self.var_fname.get(),
                            self.var_lname.get(),
                            self.var_contact.get(),
                            self.var_email.get(),
                            self.var_securityQ.get(),
                            self.var_securityA.get(),
                            self.var_passwd.get(),
                            self.txt_UserType.get()

                        )
                    )
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Registration Successful", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


root = Tk()
obj = Register(root)
root.mainloop()