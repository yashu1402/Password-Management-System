from tkinter import ttk, Tk, Label, Button, Entry, Frame, END, Toplevel,StringVar,Checkbutton
import mysql.connector
import re
from cryptography.fernet import Fernet
import logging
import traceback

class PasswordManager():
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.logged_in_user_id = None
        self.key=b'ugXRT7d3DGkjw9_1zHYMOKpqtnZC-QBKzPDyMkLwFAE='
        self.fernet=Fernet(self.key)
        logging.basicConfig(filename='password_manager.log',level=logging.DEBUG)
        self.logger=logging.getLogger(__name__)
        
    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()    

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS INFORMATION(
                ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                USER_ID INT NOT NULL,
                APPLICATION TEXT NOT NULL,
                USERNAME VARCHAR(200),
                PASSWORD VARCHAR(500))
        ''')

            
    def encrypt_data(self,data):
        print("Encryption Key:",self.key)
        encrypted_password=self.fernet.encrypt(data.encode()).decode()
        print("Encrypted Password:",encrypted_password)
        return encrypted_password
    
    def decrypt_data(self, encrypted_data):
        try:
            print("Decryption Key:", self.key)
            print("Encrypted Data(Before Decryption):", encrypted_data)
            decrypted_password = self.fernet.decrypt(encrypted_data.encode()).decode()
            print("Decrypted Password:", decrypted_password)
            return decrypted_password
        except Exception as e:
            self.logger.error("Error decrypting password:")
            self.logger.error(traceback.format_exc())
            return None
    
    def password_strength(self, password):
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None
        symbol_error = re.search(r"\W", password) is None
        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
        return password_ok 
    
    def search_records(self, search_query,user_id):
        self.connect()
        query = "SELECT * FROM INFORMATION WHERE (APPLICATION LIKE %s OR USERNAME LIKE %s ) AND USER_ID = %s"
        self.cursor.execute(query, (f"%{search_query}%", f"%{search_query}%",user_id))
        list_records = self.cursor.fetchall()
        self.close_connection()
        return list_records
    
    def show_records(self,user_id):
        self.connect()
        query = "SELECT * FROM INFORMATION WHERE USER_ID=%s"
        self.cursor.execute(query,(user_id,))
        list_records = self.cursor.fetchall()
        self.close_connection()
        
        decrypted_records=[]
        for record in list_records:
            decrypted_password=self.decrypt_data(record[6])
            print("Decrypted Password(After Retrieval):",decrypted_password)
            decrypted_record=list(record)
            decrypted_record[6]=decrypted_password
            decrypted_records.append(tuple(decrypted_record))

        return decrypted_records
    
    def check_encryption_decryption(self):
        original_password="TestPassword123"
        encrypted_password=self.encrypt_data(original_password)
        decrypted_password=self.decrypt_data(encrypted_password)
        return original_password==decrypted_password
        
    def update_password(self, data):
        ID = data['ID']
        application = data['Application']
        username = data['Username']
        password = data['Password']
        self.connect()
        query = "UPDATE INFORMATION SET APPLICATION=%s, USERNAME=%s, PASSWORD=%s WHERE ID=%s"
        self.cursor.execute(query, (application, username, password, ID))
        self.conn.commit()
        self.close_connection()
     
    def delete_password(self, ID):
        self.connect()
        query = '''DELETE FROM INFORMATION WHERE ID=%s'''
        self.cursor.execute(query, (ID,))
        self.conn.commit()
        self.close_connection()
  
    def insert_data(self, data):
        user_id=data.get('User_ID')
        if user_id is not None:
            application = data.get('Application')
            username = data.get('Username')
            password = data.get('Password')
            encrypted_password=self.encrypt_data(password)
            print("Encrypted Password(Before Insertion):",encrypted_password)
            if not self.conn.is_connected():
                self.connect()
            if self.password_strength(password):
                insert_query = "INSERT INTO INFORMATION (User_ID,APPLICATION, USERNAME, PASSWORD) VALUES (%s,%s, %s, %s)"
                self.cursor.execute(insert_query, (user_id,application, username,encrypted_password))
                self.conn.commit()
            else:
                self.showmessage("Error","Password does not meet the criteria!!!!!")

        else:
           print("User ID not provided!!!!")
   
    def showmessage(self, title_box=None, message=None):
        TIME_TO_WAIT = 500  # in milliseconds
        root = Toplevel()
        background = 'green'
        if title_box == "Error":
            background = "red"
        root.geometry('400x50+600+200')
        root.title(title_box)
        Label(root, text=message, background=background, font=('Arial', 15), fg='black').pack(padx=4, pady=2)
        root.deiconify()
        root.after(TIME_TO_WAIT, root.destroy)
        root.mainloop()
        
    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        
        
class Window():
    
    def __init__(self, root, db,user_id):
        self.db = db
        self.root = root
        self.user_id=user_id
        self.criteria_window=None
        self.criteria_labels=[]
        self.criteria_var=[]
        self.check_var=[]
        self.root.title("Password Management System")
        self.root.geometry("900x550+40+40")
        self.root.configure(bg="#06283D")
        
        heading = Label(self.root, text="Password Management System", width=94, bg="red", font=("Arial", 20), padx=10, pady=10, justify='center', anchor="center")
        heading.grid(columnspan=4, padx=5, pady=10)
        
        self.frame = Frame(self.root, highlightbackground="black", highlightthickness=1, padx=5, pady=30)
        self.frame.grid()
       
        self.create_operation_labels()
        self.create_operation_boxes()
        self.buttons()
        
        self.search_record = Entry(self.frame,bg='lightgrey', width=30, font=('Arial', 12))
        self.search_record.grid(row=self.row_no, column=self.col_no)
        self.col_no += 1
        Button(self.frame, text="Search", bg='violet', font=("Arial", 12), width=30, command=self.search_records).grid(row=self.row_no, column=self.col_no, padx=5, pady=5)
        self.create_records_tree()

    def create_operation_labels(self):
        self.col_no, self.row_no = 0, 0
        labels_info = ('ID', 'Application Name', 'Username', 'Password')
        for label_info in labels_info:
            Label(self.frame, text=label_info, bg='indigo', fg='yellow', font=("Arial", 12), padx=5, pady=2).grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no += 1
            
    def buttons(self):
        self.row_no += 1
        self.col_no = 0
        buttons_info = (('Save', 'green', self.save_password), ('Update', 'blue', self.update_password), ('Delete', 'red', self.delete_password), ('Copy Password', 'orange', self.copy_password), ('Show Records', 'dark blue', self.show_records))
        for button_info in buttons_info:
            if button_info[0] == 'Show Records':
                self.row_no += 1
                self.col_no = 0
            Button(self.frame, text=button_info[0], bg=button_info[1], fg='white', font=("Arial", 12), padx=2, pady=1, width=30, command=button_info[2]).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)
            self.col_no += 1
     
    def search_records(self):
        query = self.search_record.get()
        if query:
            for item in self.records_tree.get_children():
                self.records_tree.delete(item)
            record_lists = self.db.search_records(query,self.user_id)
            if record_lists:
                for record in record_lists:
                    self.records_tree.insert('', END, values=(record[0], record[4], record[5],record[6]))
        else:
            self.show_records()
            
    def create_operation_boxes(self):
        self.row_no += 1
        self.operations = []
        self.col_no = 0
        for i in range(4):
            show = ""
            if i == 3:
                show = "*"
            operation = Entry(self.frame, width=40, background="lightgrey", font=("Arial", 12), show=show)
            operation.grid(row=self.row_no, column=self.col_no, padx=10, pady=2)
            if i==3:
                operation.bind("<FocusIn>",self.check_criteria)
                operation.bind("<FocusOut>",self.hide_criteria_popup)
            self.operations.append(operation)
            self.col_no += 1
            
    def check_criteria(self, event):
        criteria = ["At least 8 characters", "At least 1 digit", "At least 1 uppercase letter", "At least 1 lowercase letter", "At least 1 symbol"]
        entry = event.widget
        criteria_popup = Toplevel(self.root)
        criteria_popup.title("Password Criteria")
        criteria_popup.geometry("400x180")
        criteria_popup.attributes("-topmost", True)
        criteria_popup.protocol("WM_DELETE_WINDOW", lambda: self.hide_criteria_popup(criteria_popup))
        
        criteria_var = []
        check_var = []
        for i in range(len(criteria)):
            var = StringVar()
            var.set(criteria[i])
            criteria_var.append(var)
            check_var.append(StringVar())
            Checkbutton(criteria_popup, textvariable=var, variable=check_var[i], onvalue="Checked", offvalue="").grid(row=i, column=0, sticky="w")
        
        entry.bind("<KeyRelease>", lambda event, criteria_var=criteria_var, check_var=check_var, popup=criteria_popup: self.update_criteria(event, criteria_var, check_var, popup))
    
    def update_criteria(self, event, criteria_var, check_var, popup):
        entry = event.widget
        password = entry.get()
        all_checked=all(check_var[i].get()=="Checked" for i in range(len(check_var)))
        if all_checked:
            popup.withdraw()
            return
        
        for i in range(len(criteria_var)):
            if check_var[i].get() == "":
                if i == 0 and len(password) >=8 :
                    criteria_var[i].set("✓ At least 8 characters")
                    check_var[i].set("Checked")
                elif i == 1 and any(char.isdigit() for char in password):
                    criteria_var[i].set("✓ At least 1 digit")
                    check_var[i].set("Checked")
                elif i == 2 and any(char.isupper() for char in password):
                    criteria_var[i].set("✓ At least 1 uppercase letter")
                    check_var[i].set("Checked")
                elif i == 3 and any(char.islower() for char in password):
                    criteria_var[i].set("✓ At least 1 lowercase letter")
                    check_var[i].set("Checked")
                elif i == 4 and any(not char.isalnum() for char in password):
                    criteria_var[i].set("✓ At least 1 symbol")
                    check_var[i].set("Checked")
                else:
                    all_checked=False
         
    
    def hide_criteria_popup(self,event):
        self.criteria_window.destroy()

    def save_password(self):
        application = self.operations[1].get()
        username = self.operations[2].get()
        password = self.operations[3].get()
        
        if application and username and password:
                password=self.db.encrypt_data(password)
                data = {'User_ID':self.user_id,'Application': application, 'Username': username, 'Password': password}
                self.db.insert_data(data)
                self.show_records()
                for operation in self.operations[1:]:
                    operation.delete(0,END)
              
        else:
            self.showmessage("Error","Please fill all fields")
    
    def update_password(self):
        ID = self.operations[0].get()
        application = self.operations[1].get()
        username = self.operations[2].get()
        password = self.operations[3].get()
        
        data = {'ID': ID, 'Application': application, 'Username': username, 'Password': password}
        self.db.update_password(data)
        self.show_records()
        
        for operation in self.operations[1:]:
            operation.delete(0,END)
    
    def delete_password(self):
        ID = self.operations[0].get()
        if ID:
          self.db.delete_password(ID)
          self.show_records()
          for operation in self.operations[1:]:
              operation.delete(0,END)
        else:
            self.showmessage("Error","Please select a record to delete!!!")
    
    def copy_password(self):
        password = self.operations[3].get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.showmessage("Copy", "Password Copied")
        else:
            self.showmessage("Error", "Box is Empty")
    
    def showmessage(self, title_box=None, message=None):
        TIME_TO_WAIT = 500  # in milliseconds
        root = Toplevel(self.root)
        background = 'green'
        if title_box == "Error":
            background = "red"
        root.geometry('200x30+600+200')
        root.title(title_box)
        Label(root, text=message, background=background, font=('Arial', 15), fg='black').pack(padx=4, pady=2)
        root.deiconify()
        root.after(TIME_TO_WAIT, root.destroy)
        root.mainloop()
    
    def show_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
    
        record_lists = self.db.show_records(self.user_id)
    
        for record in record_lists:
            encrypted_password = record[6]
            decrypted_password = self.db.decrypt_data(encrypted_password)  # Decrypt the password
            
            if decrypted_password:
                self.records_tree.insert('', END, values=(record[0], record[4], record[5], decrypted_password))
            else:
                self.records_tree.insert('', END, values=(record[0], record[4], record[5], 'Password Not Available'))
                
    def create_records_tree(self):
        columns = ('ID', 'Application', 'Username', 'Password')
        self.records_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.records_tree.heading('ID', text="ID")
        self.records_tree.heading('Application', text="Application Name")
        self.records_tree.heading('Username', text="Username")
        self.records_tree.heading('Password', text="Password")
        self.records_tree['displaycolumns'] = ('Application', 'Username')
        
        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                record = item['values']
                for operation, item in zip(self.operations, record):
                    operation.delete(0, END)
                    operation.insert(0, item)
                    
        self.records_tree.bind('<<TreeviewSelect>>', item_selected)
        self.records_tree.grid()
            
if __name__ == "__main__":
    user_id=1
    db_class = PasswordManager('localhost', 'root', '12345', 'password')
    db_class.connect()
    db_class.create_table()
    
    if db_class.check_encryption_decryption():
        print("Encryption and Decryption are working correctly!")
    else:
        print("Encryption and Decryption are not working correctly!")
    
    
    root = Tk()
    root_class = Window(root, db_class,user_id)
    root.mainloop()
    db_class.close_connection()