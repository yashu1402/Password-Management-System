from tkinter import *
from tkinter import messagebox
import mysql.connector

background = "#06283D"
framebg = "#EDEGED"
framefg = "#06283D"

button_mode = True
def login_user():
     root.destroy()
     import Login
     Login.open_registration()
     
def register_user(user_id):
    global root
    def register():
        username = user.get()
        password = pw.get()
        if (username == "" or username == "User ID") or (password == "" or password == "Password"):
            messagebox.showerror("Entry Error!", "Type Username or Password!!!")
        else:
            try:
                mydb = mysql.connector.connect(host='localhost', username='root', password='12345')
                mycursor = mydb.cursor()
                print("Connection Established!!")

            except:
                messagebox.showerror("Connection", "Database connection not established")

            try:
                command = "create database details"
                mycursor.execute(command)

                command = "use details"
                mycursor.execute(command)

                command = "create table login_info(ID int auto_increment not null, Username varchar(50),Password varchar(100))"
                mycursor.execute(command)

            except:
                mycursor.execute("use details")
                mydb = mysql.connector.connect(host='localhost', username='root', password='12345', database='details')
                mycursor = mydb.cursor()

                command = "insert into login_info(Username,Password) values(%s,%s)"
                mycursor.execute(command, (username, password))
                messagebox.showinfo("Register", "New User Added Succesfully!!!!!")
                mydb.commit()
                mydb.close()

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
            user.insert(0, 'User Id')

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
    Backbutton = Button(root, image=backbuttonimage, fg="#deeefb",command=login_user)
    Backbutton.place(x=20, y=15)

    root.mainloop()

if __name__ == "__main__":
    user_id=1
    register_user(user_id)