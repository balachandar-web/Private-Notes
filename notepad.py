
from tkinter import *
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="example")
cursor = conn.cursor()

# Create the Notes table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Notes (
        ID INTEGER PRIMARY KEY AUTO_INCREMENT,
        NAME TEXT NOT NULL,
        CONTENT TEXT NOT NULL,
        PRIORITY INTEGER NOT NULL,
        PASSWD TEXT NOT NULL
    );
""")
conn.commit()

def add():
    top = Toplevel()
    top.title('Add New Note')
    top.geometry("+30+150")

    Label(top, text='Name:', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    name_entry = Entry(top, font=('Arial', 12))
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    Label(top, text='Priority:', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    priority_entry = Entry(top, font=('Arial', 12))
    priority_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    Label(top, text='Password:', font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    passwd_entry = Entry(top, show="*", font=('Arial', 12))
    passwd_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    Label(top, text='Content:', font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    content_entry = Text(top, width=30, height=5, font=('Arial', 12))
    content_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    def save():
        name = name_entry.get()
        priority = priority_entry.get()
        content = content_entry.get("1.0", END)
        passwd = passwd_entry.get()

        cursor.execute("""
            INSERT INTO Notes (NAME, CONTENT, PRIORITY, PASSWD)
            VALUES (%s, %s, %s, %s)
        """, (name, content, priority, passwd))
        conn.commit()
        top.destroy()
        list_notes()

    Button(top, text='Save', command=save, font=('Arial', 12)).grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

def list_notes():
    myLis.delete(0, END)
    cursor.execute("SELECT ID, NAME FROM Notes")
    for row in cursor.fetchall():
        myLis.insert(END, f"{row[0]} - {row[1]}")

def search():
    search_term = search_entry.get()
    myLis.delete(0, END)
    cursor.execute("SELECT ID, NAME FROM Notes WHERE NAME LIKE %s", (f"%{search_term}%",))
    for row in cursor.fetchall():
        myLis.insert(END, f"{row[0]} - {row[1]}")

def delete_note():
    selected_note = myLis.get(myLis.curselection())
    note_id = selected_note.split()[0]

    top = Toplevel()
    top.title('Delete Note')
    top.geometry("+850+500")

    Label(top, text='Password:', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    passwd_entry = Entry(top, show="*", font=('Arial', 12))
    passwd_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    def check_password():
        passwd = passwd_entry.get()
        cursor.execute("SELECT PASSWD FROM Notes WHERE ID = %s", (note_id,))
        correct_passwd = cursor.fetchone()[0]
        if passwd == correct_passwd:
            cursor.execute("DELETE FROM Notes WHERE ID = %s", (note_id,))
            conn.commit()
            top.destroy()
            list_notes()
        else:
            messagebox.showerror("Error", "Incorrect Password")

    Button(top, text='ok', command=check_password, font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=5, sticky="w")


def read_note():
    selected_note = myLis.get(myLis.curselection())
    note_id = selected_note.split()[0]

    top = Toplevel()
    top.title('Read Note')
    top.geometry("+850+500")

    def display_note_content(content):
        top.geometry("+300+220")
        text_widget = Text(top, width=40, height=10, font=('Arial', 12))
        text_widget.insert(END, content)
        text_widget.config(state='disabled')
        #text_widget.config(readonlybackground='white')
        text_widget.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        Button(top, text='Edit', command=lambda: update_content(content, note_id), font=('Arial', 12)).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    def check_password():
        passwd = passwd_entry.get()
        cursor.execute("SELECT PASSWD, CONTENT FROM Notes WHERE ID = %s", (note_id,))
        result = cursor.fetchone()
        correct_passwd, content = result[0], result[1]
        if passwd == correct_passwd:
            display_note_content(content)
            # Hide password label, password entry box, and ok button
            passwd_label.grid_forget()
            passwd_entry.grid_forget()
            ok_button.grid_forget()
        else:
            messagebox.showerror("Error", "Incorrect Password")

    def update_content(old_content, note_id):
        top.destroy()
        edit_window = Toplevel()
        edit_window.geometry("+350+220")
        edit_window.title('Edit Note')

        Label(edit_window, text='Content:', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        content_entry = Text(edit_window, width=30, height=5, font=('Arial', 12))
        content_entry.insert(END, old_content)
        content_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        def save_update():
            new_content = content_entry.get("1.0", END)
            cursor.execute("UPDATE Notes SET CONTENT = %s WHERE ID = %s", (new_content, note_id))
            conn.commit()
            edit_window.destroy()
            list_notes()

        Button(edit_window, text='Update', command=save_update, font=('Arial', 12)).grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")


    passwd_label = Label(top, text='Password:', font=('Arial', 12))
    passwd_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    passwd_entry = Entry(top, show="*", font=('Arial', 12))
    passwd_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    ok_button = Button(top, text='ok', command=check_password, font=('Arial', 12))
    ok_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")


# Main window
master = Tk()
master.title('Note Taking App')

# Configure window to open in fullscreen
master.attributes('-alpha', True)

# Configure rows and columns to expand with window size
for i in range(30):
    master.grid_rowconfigure(i, weight=1)
for i in range(30):
    master.grid_columnconfigure(i, weight=1)

# Widgets

Label(master, text='PRIVATE NOTES', font=('Arial', 20, 'bold'), fg='white', bg='black').grid(row=0, column=0, columnspan=30, pady=10, sticky="nsew")

Label(master, text='Add New Note:', font=('Arial', 16)).grid(row=1, column=1, padx=0, pady=10, sticky="w")
Button(master, text='Add', command=add, font=('Arial', 12)).grid(row=1, column=2, padx=0, pady=10, sticky="w")

Label(master, text='Search Notes:', font=('Arial', 16)).grid(row=1, column=25, padx=10, pady=10, sticky="e")
search_entry = Entry(master, font=('Arial', 12))
search_entry.grid(row=1, column=26, padx=10, pady=10, sticky="e")
Button(master, text='Search', command=search, font=('Arial', 12)).grid(row=1, column=27, padx=10, pady=10, sticky="e")

Label(master, text='Notes:', font=('Arial', 16)).grid(row=2, column=25, padx=10, pady=10, sticky="w")
myLis = Listbox(master, width=10, height=10, font=('Arial', 12))
myLis.grid(row=3, column=25, columnspan=6, padx=10, pady=10, sticky="nsew")

scrollbar = Scrollbar(master, orient=VERTICAL, command=myLis.yview)
scrollbar.grid(row=3, column=29, sticky="ns")
myLis.config(yscrollcommand=scrollbar.set)

Button(master, text='Delete', command=delete_note, font=('Arial', 12)).grid(row=4, column=26, padx=10, pady=10, sticky="w")
Button(master, text='Read', command=read_note, font=('Arial', 12)).grid(row=4, column=26, padx=100, pady=10, sticky="w")

list_notes()

master.mainloop()
