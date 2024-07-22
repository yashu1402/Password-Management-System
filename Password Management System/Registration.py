from tkinter import *
from tkinter import messagebox
import mysql.connector

background = "#06283D"
framebg = "#EDEGED"
framefg = "#06283D"

button_mode = True

def login_user():
    root.destroy()
    try:
        import Login
        Login.open_registration()
    except ModuleNotFoundError:
        messagebox.showerror("Module Error", "Login module not found")
    except AttributeError:
        messagebox.showerror("Function Error", "open_registration function not found in Login module")

def register_user(user_id):
    global root
    def register():
        username = user.get()
        password = pw.get()
        email = email_entry.get()
        if (username == "" or username == "User ID") or (password == "" or password == "Password") or (email == "" or email == "Email"):
            messagebox.showerror("Entry Error!", "Type Username, Password, and Email!!!")
        else:
            try:
                mydb = mysql.connector.connect(host='localhost', username='root', password='12345')
                mycursor = mydb.cursor()
                print("Connection Established!!")

                try:
                    mycursor.execute("CREATE DATABASE IF NOT EXISTS details")
                    mycursor.execute("USE details")
                    mycursor.execute("""
                        CREATE TABLE IF NOT EXISTS login_info (
                            ID INT AUTO_INCREMENT NOT NULL,
                            Email VARCHAR(100) UNIQUE,
                            Username VARCHAR(50),
                            Password VARCHAR(100),
                            PRIMARY KEY(ID)
                        )
                    """)

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                    return

                command = "INSERT INTO login_info (Email, Username, Password) VALUES (%s, %s, %s)"
                mycursor.execute(command, (email, username, password))
                mydb.commit()
                messagebox.showinfo("Register", "New User Added Successfully!!!!!")
                mydb.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Connection", f"Database connection not established: {err}")

    root = Tk()
    root.title("New User Registration")
    root.geometry("1250x700+210+100")
    root.config(bg=background)
    root.resizable(False, False)

    # icon image
    image_icon = PhotoImage(file="icon.png")
    root.iconphoto(False, image_icon)

    # background image
    frame = Frame(root, bg="red")
    frame.pack(fill=Y)
    backgroundimage = PhotoImage(file="register.png")
    Label(frame, image=backgroundimage).pack()

    # User entry
    def user_enter(e):
        user.delete(0, 'end')

    def user_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'User ID')

    user = Entry(frame, width=18, fg='#fff', bg="#375174", border=0, font=('Arial Bold', 20))
    user.insert(0, "User ID")
    user.bind("<FocusIn>", user_enter)
    user.bind("<FocusOut>", user_leave)
    user.place(x=500, y=380)

    # Password entry
    def password_enter(e):
        pw.delete(0, 'end')

    def password_leave(e):
        if pw.get() == '':
            pw.insert(0, 'Password')

    pw = Entry(frame, width=18, fg='#fff', bg="#375174", border=0, font=('Arial Bold', 20))
    pw.insert(0, "Password")
    pw.bind("<FocusIn>", password_enter)
    pw.bind("<FocusOut>", password_leave)
    pw.place(x=500, y=470)

    # Email entry
    def email_enter(e):
        email_entry.delete(0, 'end')

    def email_leave(e):
        if email_entry.get() == '':
            email_entry.insert(0, 'Email')

    email_entry = Entry(frame, width=18, fg='#fff', bg="#375174", border=0, font=('Arial Bold', 20))
    email_entry.insert(0, "Email")
    email_entry.bind("<FocusIn>", email_enter)
    email_entry.bind("<FocusOut>", email_leave)
    email_entry.place(x=500, y=290)

    # Button to toggle password visibility
    def hide():
        global button_mode
        if button_mode:
            eyeButton.config(image=closeeye, activebackground="white")
            pw.config(show="*")
            button_mode = False
        else:
            eyeButton.config(image=openeye, activebackground="white")
            pw.config(show="")
            button_mode = True

    openeye = PhotoImage(file="openeye.png")
    closeeye = PhotoImage(file="close eye.png")
    eyeButton = Button(root, image=openeye, bg="#375174", bd=0, command=hide)
    eyeButton.place(x=780, y=470)

    # Registration button
    regis_button = Button(root, text="ADD NEW USER", bg="#455c88", fg="white", width=13, height=1, font=("Arial", 16, "bold"), bd=0, command=register)
    regis_button.place(x=530, y=600)

    # Back button
    backbuttonimage = PhotoImage(file="backbutton.png")
    Backbutton = Button(root, image=backbuttonimage, fg="#deeefb", command=login_user)
    Backbutton.place(x=20, y=15)

    root.mainloop()

if __name__ == "__main__":
    user_id = 1
    register_user(user_id)
