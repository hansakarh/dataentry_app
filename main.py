from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

INDEX = 0

window = Tk()
window.title("Student Registration Application")
window.resizable(False, False)


# --------------------Add Data To Tabel---------------#
def add_data():
    global INDEX
    gender = Gender_entry_combobox.get()
    firstname = first_entry.get()
    lastname = last_entry.get()
    age = age_entry.get()
    INDEX += 1

    if firstname and lastname and gender:
        if age.isdigit():
            tabel.insert("", 0, values=(INDEX, gender, firstname, lastname, age))

            # -----------Save to Database-------#
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS User_Information_Tabel "
                           "(ID INT, Gender TEXT, First_Name TEXT, Last_Name TEXT, Age INTEGER)")

            data_insert_query = ("INSERT INTO User_Information_Tabel(ID, Gender, First_Name, Last_Name, Age) "
                                 "VALUES (?, ?, ?, ?, ?)")

            data_insert_tuple = (INDEX, gender, firstname, lastname, age)

            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()
            # Clear Entries
            clear_entries()
        else:
            messagebox.showwarning(title="Error", message="Please enter a number as age!")

    else:
        messagebox.showwarning(title="Oops! Error", message="You Missed Some Fields!")


def load_data():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    tabel.delete(*tabel.get_children())

    cursor.execute("""SELECT * FROM User_Information_Tabel""")
    for row in cursor.fetchall():
        tabel.insert("", "end", values=row)

    conn.close()


def delete_selected_rows():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    selected_items = tabel.selection()

    for item in selected_items:
        item_id = tabel.item(item, "values")[0]

        cursor.execute("""DELETE FROM User_Information_Tabel WHERE ID = ?""", (item_id,))

        tabel.delete(item)
    conn.commit()
    conn.close()


def clear_entries():
    Gender_entry_combobox.delete(0, "end")
    first_entry.delete(0, "end")
    last_entry.delete(0, "end")
    age_entry.delete(0, "end")


def update_data():
    selected_items = tabel.selection()
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    for item in selected_items:
        item_id = tabel.item(item, "values")[0]

        cursor.execute("""DELETE FROM User_Information_Tabel WHERE Gender = ?""", (item_id,))

        tabel.delete(item)
    conn.commit()
    conn.close()
    add_data()
    clear_entries()


def delete_row():
    seleted_row = tabel.focus()
    tabel.delete(seleted_row)
    clear_entries()


def get_selected_data(event):
    selected_row = tabel.focus()
    update_data_button.config(state=NORMAL)
    values = tabel.item(selected_row, "values")
    # save_id = values[0]
    # print(save_id)

    if values:
        # tabel.insert("", 0, save_id)
        gender_index = Gender_combobox_options.index(values[1])
        Gender_entry_combobox.current(gender_index)
        first_entry.delete(0, "end")
        first_entry.insert(0, values[2])
        last_entry.delete(0, "end")
        last_entry.insert(0, values[3])
        age_entry.delete(0, "end")
        age_entry.insert(0, values[4])


def close_window():
    window.destroy()


def another_window():
    acadamic_data_window = Toplevel(window)
    acadamic_data_window.title("Acadamic Records")


# --------------------Frames-------------------------------#
mainframe = Frame(window)
mainframe.pack()

user_information_frame = LabelFrame(mainframe, text="Basic Information Of The Student")
user_information_frame.grid(row=0, column=0, padx=20, pady=20)

tabel_view_frame = LabelFrame(mainframe, text="Data Tabel")
tabel_view_frame.grid(row=0, column=1, padx=20, pady=20)

# ----------------------Labels------------------------------#
first_label = Label(user_information_frame, text="First Name")
first_label.grid(row=0, column=0)
first_entry = Entry(user_information_frame)
first_entry.grid(row=1, column=0)

last_label = Label(user_information_frame, text="Last Name")
last_label.grid(row=0, column=1)
last_entry = Entry(user_information_frame)
last_entry.grid(row=1, column=1)

age_label = Label(user_information_frame, text="Age")
age_label.grid(row=2, column=0)
age_entry = Entry(user_information_frame)
age_entry.grid(row=3, column=0)

Gender_label = Label(user_information_frame, text="Gender")
Gender_label.grid(row=0, column=2)
Gender_combobox_options = ["Male", "Female"]
Gender_entry_combobox = ttk.Combobox(user_information_frame, values=Gender_combobox_options)
Gender_entry_combobox.grid(row=1, column=2)

# ---------------------Buttons----------------------#
add_data_button = Button(user_information_frame, text="Add Data", command=add_data)
add_data_button.grid(row=4, column=0, sticky="ew")

update_data_button = Button(user_information_frame, text="Update Data", command=update_data)
update_data_button.grid(row=4, column=1, sticky="ew")
update_data_button.config(state=DISABLED)

close_window_button = Button(user_information_frame, text="Exit", command=close_window)
close_window_button.grid(row=4, column=2, sticky="ew")

delete_row_button = Button(tabel_view_frame, text="Delete", command=delete_selected_rows)
delete_row_button.grid(row=1, column=0, sticky="ew", padx=10, pady=20)

load_data_button = Button(user_information_frame, text="Load Data", command=load_data)
load_data_button.grid(row=5, column=0, sticky="ew")

clear_entries_button = Button(user_information_frame, text="Clear Entries", command=clear_entries)
clear_entries_button.grid(row=5, column=1, sticky="ew")

for widget in user_information_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# ---------------------Tabel----------------------#
tabel = ttk.Treeview(tabel_view_frame, columns=("ID", "Gender", "First Name", "Last Name", "Age"), show="headings")
tabel.heading("ID", text="ID")
tabel.heading("Gender", text="Gender")
tabel.heading("First Name", text="First Name")
tabel.heading("Last Name", text="Last Name")
tabel.heading("Age", text="Age")
tabel.column("ID", width=20, stretch=NO, anchor=CENTER)
tabel.column("Gender", width=60, minwidth=60, stretch=NO, anchor=CENTER)
tabel.column("Age", width=60, minwidth=60, stretch=NO, anchor=CENTER)
tabel.column("First Name", anchor=CENTER)
tabel.column("Last Name", anchor=CENTER)
tabel.column("Gender", anchor=CENTER)

tabel.grid(row=0, column=0, padx=10, pady=10)
tabel.bind("<<TreeviewSelect>>", get_selected_data)

window.mainloop()
