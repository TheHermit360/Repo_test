"""This app creates a json file from which it registers, updates and removes items."""

import os
from tkinter import *
from tkinter import messagebox
import random
import string
import secrets
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():

    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password_random = ''.join(random.SystemRandom().choice(alphabet) for _ in range(20))
    password_secrets = ''.join(secrets.choice(password_random) for _ in range(15))
    password_list = [password_secrets]
    random.shuffle(password_list)
    password = ""
    for i in password_list:
        password += i
    password_line.insert(0, f"{password}")
    pyperclip.copy(password)  # auto-copies the pass to the clipboard, ready to use


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_line.get()
    email = email_username_line.get()
    password = password_line.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Ops", message="Fill all the lines.")
    else:
        try:
            with open("pw_lst.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("pw_lst.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            if website in data:
                answer = messagebox.askyesno(title="Confirm update",
                                             message=f"{website} exists already, do you wish to update it?")
                if answer:
                    # Updating old data with new data
                    data.update(new_data)

                    with open("pw_lst.json", "w") as data_file:
                        # Saving updated data
                        json.dump(data, data_file, indent=4)
                        messagebox.showinfo(title="Updated", message=f"{website} successfully updated.")
            else:
                data.update(new_data)

                with open("pw_lst.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
                    messagebox.showinfo(title="Added", message=f"{website} successfully added.")
        finally:
            website_line.delete(0, END)
            email_username_line.delete(0, END)
            password_line.delete(0, END)


# ---------------------------- SEARCH ITEM ------------------------------- #
def search_password():

    website = website_line.get()
    try:
        with open("pw_lst.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Attention!", message="There are no lists where to search.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Error", message=f"{website} does not exist.")


# ---------------------------- DEL ITEM ------------------------------- #
def del_key():
    """It removes an item from json data"""

    website = website_line.get()
    answer = messagebox.askyesno(title="Confirm cancellation",
                                 message=f"Are you sure you want to delete {website}?")

    if answer:
        try:
            with open("pw_lst.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No json file found.")
        else:
            if website in data:
                del data[website]
                with open("pw_lst.json", "w") as data_file:
                    json.dump(data, data_file)
                    messagebox.showinfo(title=f"{website} removed", message=f"{website} successfully removed.")
            else:
                messagebox.showinfo(title="Error", message=f"{website} does not exist.")


# ---------------------------- OPEN FILE DIRECTORY ------------------------------- #
def opendir():
    cwd = os.getcwd()  # Get the current working directory
    os.startfile(cwd)


# ---------------------------- UI SETUP ------------------------------- #

# Tk init:
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=25)
window.resizable(width=False, height=False)

# Labels:
website_label = Label(text="Website:", font=('Arial', 10, 'bold'))
website_label.grid(row=1, column=0, sticky=W)

email_username_label = Label(text="Email/ID:", font=('Arial', 10, 'bold'))
email_username_label.grid(row=2, column=0, sticky=W)

password_label = Label(text="Password:", font=('Arial', 10, 'bold'))
password_label.grid(row=3, column=0, sticky=W)

# Entries:
website_line = Entry(width=35)
website_line.grid(row=1, column=1, columnspan=2)
website_line.focus()

email_username_line = Entry(width=35)
email_username_line.grid(row=2, column=1, columnspan=2)

password_line = Entry(width=35)
password_line.grid(row=3, column=1, columnspan=2)

# Buttons:
search_button = Button(text="Search", width=25, command=search_password)
search_button.grid(row=6, column=1, pady=2)

del_button = Button(text="Remove", width=25, command=del_key)
del_button.grid(row=7, column=1, pady=2)

generate_pass_button = Button(text="Generate Password", width=25, command=password_generator)
generate_pass_button.grid(row=4, column=1, pady=2)

add_button = Button(text="Add", width=25, command=save)
add_button.grid(row=5, column=1, pady=2)

opendir_button = Button(text="Open", width=25, command=opendir)
opendir_button.grid(row=8, column=1, pady=2)

# Code end
window.mainloop()
