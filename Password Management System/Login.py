from tkinter import *
from tkinter import messagebox
import mysql.connector
from password_management_system import PasswordManager
import Registration  # Import the Registration module
import random


background = "#06283D"
framebg = "#EDEGED"
framefg = "#06283D"

trials = 0
user_id = 1

def trial():
    global trials
    trials += 1
    print("Trial Number is", trials)
    if trials == 3:
        messagebox.showwarning("Warning", "Last Chance to login!!!")
        root.destroy()

'''def send_otp_via_email(email):
    sender_email = "yogesh.choudhary.2021@ecajmer.ac.in"
    sender_password = "dhaeopvxbozvswna"
    
    otp = ''.join(random.choices('0123456789', k=6))
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'OTP Verification'
    
    body = f'Your OTP is: {otp}'
    message.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        print(f"OTP sent to {email}")
        return otp
    except Exception as e:
        print(str(e))
        return None
    
def open_otp_verification_window():
    otp_window = Toplevel(root)
    otp_window.title("OTP Verification")
    otp_window.geometry("400x200")
    otp_window.config(bg=background)
    
    otp_label = Label(otp_window, text="Enter OTP:", fg="#fff", bg=background, font=("Arial", 16))
    otp_label.pack(pady=10)
    
    otp_entry = Entry(otp_window, width=20, fg='#fff', bg="#375174", font=('Arial Bold', 16), show="*")
    otp_entry.pack(pady=10)
    
    verify_button = Button(otp_window, text="VERIFY", bg="#1f5675", fg="white", width=10, height=1, font=("Arial", 14, 'bold'), bd=0, command=lambda: validate_otp(otp_entry.get(), otp_window))
    verify_button.pack(pady=10)

def validate_otp(otp_entered, otp_window):
    actual_otp = send_otp_via_email(email_entry.get())
    if otp_entered == actual_otp:
        messagebox.showinfo("Success", "OTP validated successfully!!!")
        otp_window.destroy()
        root.destroy()
        open_password_management_system()
    else:
        messagebox.showerror("Error", "Invalid OTP. Please try again.")
        otp_entry.delete(0, 'end')'''

def loginuser():
    global root
    global user_id
    username = user.get()
    password = pw.get()
    #email = email_entry.get()

    if (username == "" or username == "User Id") or (password == "" or password == "Password"):
        messagebox.showerror("Entry error", "Type username or password!!")
    #elif email == "" or email == "Email":
     #   messagebox.showerror("Entry Error", "Type Email!!")
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
            messagebox.showinfo("Login", "Successfully Login!!!!")
            root.destroy()
            open_password_management_system()
           # open_otp_verification_window()

def open_password_management_system(): 
    import password_management_system
    root=Tk()
    db_class=PasswordManager('localhost','root','12345','password')
    db_class.connect()
    db_class.create_table()
    root_class=password_management_system.Window(root, db_class,user_id)
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

'''# Entry for email
def email_enter(e):
    email_entry.delete(0, 'end')

def email_leave(e):
    email = email_entry.get()
    if email == '':
        email_entry.insert(0, 'Email')

email_entry = Entry(frame, width=18, fg='#fff', border=0, bg="#375174", font=('Arial Bold', 20),justify='center')
email_entry.insert(0, "Email")
email_entry.bind("<FocusIn>", email_enter)
email_entry.bind("<FocusOut>", email_leave)
email_entry.place(x=500, y=530)'''                         

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

# Label and button for registration
label = Label(root, text="Don't have an account?", fg="#fff", bg="#00264d", font=("Microsoft YaHei UI Light", 9))
label.place(x=500, y=500)

registerButton = Button(root, width=10, text="Add New User", border=0, bg="#00264d", cursor='hand2', fg='#57a1f8', command=open_registration)
registerButton.place(x=650, y=500)

root.mainloop()