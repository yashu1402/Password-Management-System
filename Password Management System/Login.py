from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import Registration
from password_management_system import PasswordManager

background = "#06283D"
framebg = "#EDEGED"
framefg = "#06283D"

trials = 0
user_id = 1
otp = None
email = None

smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'kudiyayash31@gmail.com'
sender_password = 'blxx sdpn ahwt mifa'

def send_otp():
    global otp, email
    email = email_entry.get()
    username = user.get()
    if email == "" or email == "Email":
        messagebox.showerror("Entry error", "Type your email!!")
        return

    if username == "" or username == "User Id":
        messagebox.showerror("Entry error", "Type your User Id!!")
        return

    try:
        mydb = mysql.connector.connect(host='localhost', username='root', password='12345', database="details")
        mycursor = mydb.cursor()
        print("Connection Established")

        mycursor.execute("SELECT Email FROM login_info WHERE Username=%s", (username,))
        myresult = mycursor.fetchone()
        if myresult is None:
            messagebox.showerror("Error", "Username not found")
            return

        stored_email = myresult[0]
        if email != stored_email:
            messagebox.showerror("Error", "Email does not match the one registered with this username")
            return

        otp = random.randint(100000, 999999)
        message = f"Your OTP for login is {otp}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'OTP for Login'
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()

        messagebox.showinfo("OTP Sent", f"OTP has been sent to {email}")
        show_otp_window()

    except mysql.connector.Error as err:
        messagebox.showerror("Connection Error", f"Database connection not established: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

def trial():
    global trials
    trials += 1
    print("Trial Number is", trials)
    if trials == 3:
        messagebox.showwarning("Warning", "Last Chance to login!!!")
        root.destroy()

def loginuser():
    global root, user_id
    username = user.get()
    password = pw.get()

    if (username == "" or username == "User Id") or (password == "" or password == "Password"):
        messagebox.showerror("Entry error", "Type username or password!!")
    else:
        try:
            mydb = mysql.connector.connect(host='localhost', username='root', password='12345', database="details")
            mycursor = mydb.cursor()
            print("Connection Established")

        except:
            messagebox.showerror("Connection", "Database connection not established!!")

        command = "use details"
        mycursor.execute(command)
        command = "select * from login_info where Username=%s and Password=%s"
        mycursor.execute(command, (username, password))
        myresult = mycursor.fetchone()
        print(myresult)

        if myresult == None:
            messagebox.showinfo("Invalid", "Invalid userid and password!!")
            trial()

        else:
            user_id = myresult[0]

def verify_otp():
    entered_otp = otp_entry.get()
    if str(otp) == entered_otp:
        messagebox.showinfo("Login", "Successfully Login!!!!")
        otp_window.destroy()
        root.destroy()
        open_password_management_system()
    else:
        messagebox.showerror("Invalid", "Invalid OTP!!")
        trial()

def show_otp_window():
    global otp_window, otp_entry
    otp_window = Toplevel(root)
    otp_window.title("OTP Verification")
    otp_window.geometry("300x200")
    otp_window.config(bg=background)

    Label(otp_window, text="Enter OTP", bg=background, fg="white", font=("Arial", 14)).pack(pady=20)
    
    otp_entry = Entry(otp_window, width=20, fg='#000', bg="#fff", border=0, font=('Arial', 14))
    otp_entry.pack(pady=10)
    
    verifyButton = Button(otp_window, text="VERIFY OTP", bg="#1f5675", fg="white", width=10, height=1, font=("arial", 12, 'bold'), bd=0, command=verify_otp)
    verifyButton.pack(pady=10)

def open_password_management_system(): 
    import password_management_system
    root=Tk()
    db_class=PasswordManager('localhost','root','12345','password')
    db_class.connect()
    db_class.create_table()
    root_class=password_management_system.Window(root, db_class, user_id)
    root.mainloop()
    db_class.close_connection()

def open_registration():  # Function to open the registration window
    root.destroy()
    import Registration
    Registration.register_user(user_id)# Call the register_user function from Registration module

root = Tk()
root.title("Login Portal")
root.geometry("1250x700+210+100")
root.config(bg=background)
root.resizable(False, False)

#icon image
image_icon = PhotoImage(file='icon.png')
root.iconphoto(False, image_icon)

# background image
frame = Frame(root, bg="red")
frame.pack(fill=Y)

backgroundimage = PhotoImage(file='Login.png')
Label(frame, image=backgroundimage).pack()

# Entry for username
def user_enter(e):
    user.delete(0, 'end')

def user_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'User Id')

user = Entry(frame, width=18, fg='#fff', border=0, bg="#375174", font=('Arial Bold', 24))
user.insert(0, "UserID")
user.bind("<FocusIn>", user_enter)
user.bind("<FocusOut>", user_leave)
user.place(x=500, y=315)

# Entry for password
def password_enter(e):
     pw.delete(0, 'end')

def password_leave(e):
     if pw.get() == '':
         pw.insert(0, 'Password')

pw = Entry(frame, width=18, fg='#fff', bg="#375174", border=0, font=('Arial Bold', 20))
pw.insert(0, "Password")
pw.bind("<FocusIn>", password_enter)
pw.bind("<FocusOut>", password_leave)
pw.place(x=500, y=410)                       

# Entry for email
def email_enter(e):
    email_entry.delete(0, 'end')

def email_leave(e):
    if email_entry.get() == '':
        email_entry.insert(0, 'Email')

email_entry = Entry(frame, width=18, fg='#fff', bg="#375174", border=0, font=('Arial Bold', 23))
email_entry.insert(0, "Email")
email_entry.bind("<FocusIn>", email_enter)
email_entry.bind("<FocusOut>", email_leave)
email_entry.place(x=405, y=520)

# Button to toggle password visibility
button_mode = True

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
eyeButton.place(x=780, y=410)

# Button to login
loginButton = Button(root, text="LOGIN", bg="#1f5675", fg="white", width=10, height=1, font=("arial", 16, 'bold'), bd=0, command=loginuser)
loginButton.place(x=550, y=595)

# Button to send OTP
sendOtpButton = Button(root, text="SEND OTP", bg="#1f5675", fg="white", width=10, font=("arial", 16, 'bold'), bd=0, command=send_otp)
sendOtpButton.place(x=715, y=520)

# Label and button for registration
label = Label(root, text="Don't have an account?", fg="#fff", bg="#00264d", font=("Microsoft YaHei UI Light", 9))
label.place(x=480, y=480)

registerButton = Button(root, width=10, text="Add New User", border=0, bg="#00264d", cursor='hand2', fg='#57a1f8', command=open_registration)
registerButton.place(x=630, y=482)

root.mainloop()
