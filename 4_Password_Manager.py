'''
Author: Matthew Cao
Date:
Description:
References:
https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/
https://www.geeksforgeeks.org/how-to-change-the-tkinter-label-font-size/
https://www.geeksforgeeks.org/python-creating-a-button-in-tkinter/
https://stackoverflow.com/questions/48278853/tk-toplevel-and-winfo-toplevel-difference-between-them-and-how-and-when
https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
https://www.geeksforgeeks.org/password-validation-in-python/
https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
https://www.geeksforgeeks.org/random-numbers-in-python/
https://www.tutorialspoint.com/how-to-exit-from-python-using-a-tkinter-button
https://www.sololearn.com/Discuss/1582033/how-to-check-if-input-is-empty-in-python
https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
https://www.tutorialspoint.com/python/tk_pack.htm#:~:text=fill%20%E2%88%92%20Determines%20whether%20widget%20fills,fill%20both%20horizontally%20and%20vertically).
https://www.tutorialspoint.com/how-to-get-an-entry-box-within-a-messagebox-in-tkinter
https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-text-file-using-python
https://www.guru99.com/python-check-if-file-exists.html#:~:text=Python%20exists(),exists%20and%20returns%20false%20otherwise.
https://www.geeksforgeeks.org/fernet-symmetric-encryption-using-cryptography-module-in-python/
https://chat.openai.com/
'''

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
import re
import cryptography
from cryptography.fernet import Fernet
import os.path
from os import path

# Set up a key file for encrypting/decrypting files
if not path.exists('Key.key'):
    key = Fernet.generate_key()

    with open('Key.key', 'wb') as file:
        file.write(key)

with open('Key.key', 'rb') as file:
    key = file.read()

use_key = Fernet(key)
    
'''Classes for main window of user interface'''
# Set up layout of window
# Sources:
# https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/
# https://www.geeksforgeeks.org/how-to-change-the-tkinter-label-font-size/
class GUIMainWindow:
    def __init__(self, window):
        self.window = window
        
        # Title for window
        self.window.title('Main Menu')

        # Initialize window size
        self.window.geometry('1000x500')

        # Prevent window from being resized
        self.window.resizable(width = False, height = False)

        # Labels within window
        header = Label(window, text = 'Secure all your passwords in one place and access them whenever you want.',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)
        sub_header = Label(window, text = 'Select an option below to continue.', font = ('Times New Roman', 18))\
            .place(relx = .5, rely = .2, anchor = CENTER)
        
# Buttons within window
# Sources:
# https://www.geeksforgeeks.org/python-creating-a-button-in-tkinter/
# https://stackoverflow.com/questions/48278853/tk-toplevel-and-winfo-toplevel-difference-between-them-and-how-and-when
class GUIMainButtons:
    def __init__(self, buttons):
        self.buttons = buttons
        # Button for new users
        new_user = Button(buttons, text = 'New User', bd = '3', width = 10, height = 3, \
            font = ('Times New Roman', 12), command = self.new_user_window).place(x = 200, y = 215)
        # Button for returning users
        returning_user = Button(buttons, text = 'Returning\nUser', bd = '3', width = 10, \
            height = 3, font = ('Times New Roman', 12), command = self.returning_user_window).place \
            (relx = .5, rely = .5, anchor = CENTER)
        
        # Button to exit
        exit = Button(buttons, text = 'Exit', bd = '3', width = 10, height = 3, \
            font = ('Times New Roman', 12), command = self.exit_window).place(x = 700, y = 215)

    # Close window when exit button is clicked
    def exit_window(self):
        with open('User_Data.txt', 'rb') as file:
            data = file.read()
        decrypt = use_key.decrypt(data)
        new = decrypt.decode()
        print(new)
            
        self.buttons.destroy()
    
    # Use Toplevel widget to open a new windows when buttons in main menu are clicked
    def new_user_window(self):
        new_user_window_toplevel = Toplevel(self.buttons.winfo_toplevel())
        GUINewUserWindow(new_user_window_toplevel)
        self.buttons.iconify()

    def returning_user_window(self):
        returning_user_window_toplevel = Toplevel(self.buttons.winfo_toplevel())
        GUIReturningUserWindow(returning_user_window_toplevel)
        self.buttons.iconify()

'''Classes for saving user inputs'''  
# Save and manipulate username input
# Sources:
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
# https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
class GetUsernameInput:
    def __init__(self, username):
        self.username = username

    # Write username input to file
    def username_input(self):
        x = self.username.get()

        # Create a file for storing user data if file doesn't exist
        if not path.exists('User_Data.txt'):
            with open('User_Data.txt', 'a') as file:
                file.write('Username: ' + x + '\n')
                file.write('\n')
        # If file does exist, decrypt file, add to existing data, and rewrite file 
        else:
            with open('User_Data.txt', 'rb') as file:
                data = file.read()

            decrypt_data = use_key.decrypt(data)
            string_data = decrypt_data.decode()

            with open('User_Data.txt', 'w') as file:
                file.write(string_data + 'Username: ' + x + '\n')
            
# Save and manipulate password input
# Sources:
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
class GetPasswordInput:
    def __init__(self, password):
        self.password = password
    
    # Write password input to file
    def password_input(self):
        # Write original, unencrypted password to file
        x = self.password.get()
        user_data = open('User_Data.txt', 'a')
        user_data.write('Password: ' + x + '\n')
        user_data.close()

# Save and manipulate phone number input
# Sources:
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
class GetPhoneInput:
    def __init__(self, phone):
        self.phone = phone
    
    # Write phone input to file
    def phone_input(self):
        # Write original, unencrypted phone number to file
        x = self.phone.get()
        user_data = open('User_Data.txt', 'a')
        user_data.write('Phone: ' + x + '\n')
        user_data.close()

# Save and manipulate email address input
# Sources:
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
class GetEmailInput:
    def __init__(self, email):
        self.email = email
    
    # Write email address input to file
    def email_input(self):
        # Write original, unencrypted email address to file
        x = self.email.get()
        user_data = open('User_Data.txt', 'a')
        user_data.write('Email: ' + x + '\n')
        user_data.close()
        
'''Class for a window opened by clicking New User button'''
# Open a new window when New User button is clicked in main window
# Sources:
# https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
# https://www.geeksforgeeks.org/password-validation-in-python/
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
class GUINewUserWindow:
    def __init__(self, window):
        self.window = window
        # Used to save user inputs
        self.save_username = StringVar()
        self.save_password = StringVar()
        self.save_phone = StringVar()
        self.save_email = StringVar()
        # Title for window
        self.window.title('New User')
        # Set size of window
        self.window.geometry('800x400')
        # Prevent window from being resized
        self.window.resizable(width = False, height = False)

        # Header label
        header = Label(window, text = 'Set up your password manager account below then click done.',\
            font = ('Times New Roman', 18))
        header.place(relx = .5, rely = .1, anchor = CENTER)
        
        # Username label and entry
        username_label = Label(window, text = 'Username:', font = ('Times New Roman', 12)).place(x = 250, y = 100)
        username_entry = Entry(window, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_username).place(x = 370, y = 100)
        # Password label and entry
        password_label = Label(window, text = 'Password:', font = ('Times New Roman', 12)).place(x = 250, y = 150)
        password_entry = Entry(window, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_password).place(x = 370, y = 150)
        # Phone number label and entry
        phone_label = Label(window, text = 'Phone number:', font = ('Times New Roman', 12)).place(x = 250, y = 200)
        phone_entry = Entry(window, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_phone).place(x = 370, y = 200)
        # Email address label and entry
        email_label = Label(window, text = 'Email address:', font = ('Times New Roman', 12)).place(x = 250, y = 250)
        email_entry = Entry(window, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_email).place(x = 370, y = 250)

        # Button to complete new user account creation
        save_profile = Button(window, text = 'Save Profile', bd = '3', width = 10, height = 1, \
            font = ('Times New Roman', 12), command = self.get_inputs).place(relx = .5, rely = .85, anchor = CENTER)

        # Call classes to save inputs to file
        self.get_username = GetUsernameInput(self.save_username)
        self.get_password = GetPasswordInput(self.save_password)
        self.get_phone = GetPhoneInput(self.save_phone)
        self.get_email = GetEmailInput(self.save_email)
        
    # Function to help save inputs to file and perform input validation
    def get_inputs(self):
        # Array of special characters for password input validation
        password_symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        # Get user inputs for input validation
        check_username = self.save_username.get()
        check_password = self.save_password.get()
        check_phone = self.save_phone.get()
        check_email = self.save_email.get()
        
        # Perform input validation
        # Check validity of username
        if len(check_username) == 0:
            messagebox.showerror(title = 'Error', message = 'Username field is empty.\nPlease try again.')
        elif len(check_username) > 19:
            messagebox.showerror(title = 'Error', message = 'Username must be less than 20 characters long.\nPlease try again.')
        # Check validity of password
        elif len(check_password) == 0:
            messagebox.showerror(title = 'Error', message = 'Password field is empty.\nPlease try again.')
        elif len(check_password) < 12 or not any(char.isdigit() for char in check_password) \
            or not any(char.isupper() for char in check_password) or not any(char.islower() \
            for char in check_password) or not any(char in password_symbols for char in \
            check_password):
            messagebox.showerror(title = 'Error', message = 'Password must contain a number, uppercase letter, \nlowercase letter, special symbol (e.g., !@#$), and \nbe at least 12 characters long. Please try again.')
        # Check validity of phone number
        elif len(check_phone) == 0:
            messagebox.showerror(title = 'Error', message = 'Phone number field is empty. Please try again.')
        elif not re.match(r'^\d{10}$', check_phone):
            messagebox.showerror(title = 'Error', message = 'Phone number must be 10 digits with no dashes. Please try again.')
        # Check validity of email address
        elif len(check_email) == 0:
            messagebox.showerror(title = 'Error', message = 'Email address field is empty. Please try again.')
        elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', check_email):
            messagebox.showerror(title = 'Error', message = 'Email address invalid. Please try again.')
        else:
            # Get all user inputs
            self.get_username.username_input()
            self.get_password.password_input()
            self.get_phone.phone_input()
            self.get_email.email_input()

            # Encrypt file with user data
            with open('User_Data.txt', 'rb') as read_file:
                data = read_file.read()

            encrypt_data = use_key.encrypt(data)

            with open('User_Data.txt', 'wb') as write_file:
                write_file.write(encrypt_data)

            # Display a success message if account is created
            messagebox.showinfo(title = 'Success', \
                message = 'Your account has been saved. Click on Returning User\nin the main menu to start managing your passwords.')

            # Close the window
            self.window.destroy()

'''Classes for getting user inputs when adding new passwords to password manager'''
# Save and manipulate new password description input
# Sources:
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
class GetNewPasswordDescriptionInput:
    def __init__(self, description):
        self.description = description
        
    # Write password description to file
    def new_description_input(self):
        # Verify that password description is entered and write to file
        y = self.description.get()
        saved_passwords = open('Saved_Passwords.txt', 'a')
        saved_passwords.write('Description: ' + y)
        saved_passwords.write('\n')
        saved_passwords.close()

# Save and manipulate new password input
class GetNewPasswordInput:
    def __init__(self, password):
        self.password = password
        
    # Write new password to file
    def new_password_input(self):
        # Write original, unencrypted new password to file
        y = self.password.get()
        saved_passwords = open('Saved_Passwords.txt', 'a')
        saved_passwords.write('Password: ' + y)
        saved_passwords.write('\n')
        saved_passwords.close()

'''Class for a window opened by clicking Returning User button'''
# Open a new window when Returning User button is clicked in main window
# https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
# https://www.geeksforgeeks.org/random-numbers-in-python/
# https://www.tutorialspoint.com/how-to-exit-from-python-using-a-tkinter-button
# https://www.sololearn.com/Discuss/1582033/how-to-check-if-input-is-empty-in-python
# https://www.tutorialspoint.com/how-to-get-an-entry-box-within-a-messagebox-in-tkinter
# https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-text-file-using-python
class GUIReturningUserWindow:
    def __init__(self, window):
        self.window = window
        # Used to read user inputs
        self.read_username = StringVar()
        self.read_password = StringVar()
        # Title for window
        self.window.title('Returning User')
        # Set size of window
        self.window.geometry('800x400')
        # Prevent window from being resized
        self.window.resizable(width = False, height = False)

        # Set up frames to have multiple pages within window
        self.frame = {}
        
        # Set default frame to login page
        self.login_frame()

        # Used to read user input for adding new passwords
        self.save_new_password_description = StringVar()
        self.save_new_password = StringVar()

    # Frame for login page
    def login_frame(self):
        login_frame = Frame(self.window)
        self.frame['login_frame'] = login_frame
            
        # Header label
        header = Label(login_frame, text = 'Welcome back! Log in to manage your passwords.',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)

        # Username label and entry
        username_label = Label(login_frame, text = 'Username:', font = ('Times New Roman', 12)).place(x = 250, y = 100)
        username_entry = Entry(login_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.read_username).place(x = 370, y = 100)
        # Password label and entry
        password_label = Label(login_frame, text = 'Password:', font = ('Times New Roman', 12)).place(x = 250, y = 150)
        password_entry = Entry(login_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.read_password).place(x = 370, y = 150)

        # Button to complete login
        login = Button(login_frame, text = 'Login', bd = '3', width = 7, height = 1, \
            font = ('Times New Roman', 12), command  = self.check_close_login_frame) \
            .place(relx = .5, rely = .7, anchor = CENTER)

        # Display login frame
        login_frame.pack(fill = 'both', expand = True)

    # Check inputs from login frame and close the frame
    def check_close_login_frame(self):
        # Get username input
        entered_username = self.read_username.get()
        entered_password = self.read_password.get()

        # Open file to verify inputs
        with open('User_Data.txt', 'rb') as verify_input:
            read_data = verify_input.read()

            # Decrypt file data
            decrypt_data = use_key.decrypt(read_data)
            string_data = decrypt_data.decode()

            # Format decrypted data
            format_data = [i.strip() for i in string_data.split('\n') if i.strip()]
            final_data = '\n'.join(format_data)
            
            # Verify inputs
            if 'Username: ' + entered_username in final_data and entered_username + '\n' + 'Password: ' + entered_password in final_data \
               and len(entered_username) != 0 and len(entered_password) != 0:
                # Close frame for login page
                self.frame['login_frame'].destroy()
                # Switch to multi-authentication frame
                self.dashboard_frame()
            else:
                # Display an error message if username or password invalid
                messagebox.showerror(title = 'Error', message = 'Incorrect username or password. Please try again.')

        print(final_data)

    # Frame to display a dashboard
    def dashboard_frame(self):
        dashboard_frame = Frame(self.window)
        self.frame['dashboard_frame'] = dashboard_frame
        
        # Header label
        header = Label(dashboard_frame, text = 'Select an option below.',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)

        # Button for new users
        view_passwords = Button(self.window, text = 'View\nPasswords', bd = '3', width = 10, height = 3, \
            font = ('Times New Roman', 12), command = self.view_passwords_frame).place(x = 150, y = 163)

        # Button for returning users
        add_passwords = Button(self.window, text = 'Add\nPasswords', bd = '3', width = 10, \
            height = 3, font = ('Times New Roman', 12), command = self.add_passwords_frame).place \
            (relx = .5, rely = .5, anchor = CENTER)
        # Button to exit
        exit = Button(self.window, text = 'Exit', bd = '3', width = 10, height = 3, \
            font = ('Times New Roman', 12), command = self.exit_window).place(x = 550, y = 163)
        
        # Display multi-authentication frame
        dashboard_frame.pack(fill = 'both', expand = TRUE)

    # Frame for user to view saved passwords
    def view_passwords_frame(self):
        # Close dashboard frame
        self.frame['dashboard_frame'].destroy()
        
        # Set up view passwords frame
        view_passwords_frame = Frame(self.window)
        self.frame['view_passwords_frame'] = view_passwords_frame

        # Header label
        header = Label(view_passwords_frame, text = 'Your list of passwords:',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)

        # Set up text and scrollbar widgets to display passwords
        text = Text(view_passwords_frame)
        text.pack(fill = BOTH)
        text.place(x = 150, y = 100, width = 500, height = 200)
        scroll = Scrollbar(text)
        scroll.config(command = text.yview)
        text.config(yscrollcommand = scroll.set)
        scroll.pack(side = RIGHT, fill = Y)

        # Decrypt saved passwords data
        with open('Saved_Passwords.txt', 'rb') as file:
            data = file.read()

        decrypt_data = use_key.decrypt(data)
        string_data = decrypt_data.decode()
        
        # Format decrypted data
        format_data = [i.strip() for i in string_data.split('\n\n') if i.strip()]
        final_data = ''.join(format_data)

        # Display user's saved passwords from file by identifying user's passwords with dividers placed within file
        read_lines = final_data.split('\n')
        find_dividers = False
        temp_data = []

        for i in read_lines:
            i = i.strip()  
            if i == self.read_username.get() + ' start':
                find_dividers = True
                continue
            elif i == self.read_username.get() + ' end':
                find_dividers = False
                continue
            if find_dividers:
                temp_data.append(i)

        # Display passwords without dividers
        print_data = '\n'.join(temp_data).replace('user2 enduser2 start', '')
        text.insert(END, print_data)

        # Button to return to dashboard frame
        back = Button(view_passwords_frame, text = 'Back', bd = '3', width = 11, height = 3, font = ('Times New Roman', 12), \
            command = lambda: [self.dashboard_frame(), self.frame['view_passwords_frame'].destroy()]).place(relx = .4, rely = .87, anchor = CENTER)

        # Button to remove passwords
        remove = Button(view_passwords_frame, text = 'Remove\nPassword', bd = '3', width = 11, height = 3, font = ('Times New Roman', 12), \
            command = self.remove_password).place(relx = .6, rely = .87, anchor = CENTER)
        
        # Display view passwords frame
        view_passwords_frame.pack(fill = 'both', expand = TRUE)

    # Function to remove a password when requested by user in GUIReturningUserWindow
    def remove_password(self):
        # Display a pop-up message asking for the password to be removed
        remove_message = askstring('Remove Password', 'Enter the password you would like to remove:')
    
        # Decrypt file with user passwords and write back to file
        if path.exists('Saved_Passwords.txt'):
            with open('Saved_Passwords.txt', 'rb') as file:
                data = file.read()

            decrypt_data = use_key.decrypt(data)
            string_data = decrypt_data.decode()
        
        # Format decrypted data and save to a variable
        format_data_1 = filter(lambda i: i.strip(), string_data.splitlines())
        format_data_2 = '\n'.join(format_data_1)

        # Remove selected password from variable and encrypt data
        password_regex = re.compile(r'user2 start\nDescription: .*\nPassword: ' + re.escape(remove_message) + r'\nuser2 end')
        new_data = password_regex.sub('\n', format_data_2)
        encrypt_data = use_key.encrypt(new_data.encode())

        # Write encrypted data back to file
        with open('Saved_Passwords.txt', 'wb') as file:
            file.write(encrypt_data)

    # Frame for user to add new passwords
    def add_passwords_frame(self):
        # Close dashboard frame
        self.frame['dashboard_frame'].destroy()
        
        # Set up add passwords frame
        add_passwords_frame = Frame(self.window)
        self.frame['add_passwords_frame'] = add_passwords_frame

        # Header label
        header = Label(add_passwords_frame, text = 'Add a new password to your password manager.',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)
        
        # New password description label and entry
        new_password_description_label = Label(add_passwords_frame, text = 'Description\n(e.g., YouTube account):', \
            font = ('Times New Roman', 12)).place(x = 200, y = 150)
        new_password_description_entry = Entry(add_passwords_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_new_password_description).place(x = 370, y = 150)

        # Adding new password label and entry
        new_password_label = Label(add_passwords_frame, text = 'Password:', font = ('Times New Roman', 12)).place(x = 250, y = 220)
        new_password_entry = Entry(add_passwords_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_new_password).place(x = 370, y = 220)

        # Button to return to dashboard frame
        back = Button(add_passwords_frame, text = 'Back', bd = '3', width = 11, height = 1, font = ('Times New Roman', 12), \
            command = lambda: [self.dashboard_frame(), self.frame['add_passwords_frame'].destroy()]).place(x = 250, y = 300)
        
        # Button to finish adding new password
        finish_new_password = Button(add_passwords_frame, text = 'Save Password', bd = '3', width = 11, height = 1, \
            font = ('Times New Roman', 12), command = self.get_inputs).place(x = 450, y = 300)

        # Call classes to save inputs
        self.get_new_password_description = GetNewPasswordDescriptionInput(self.save_new_password_description)
        self.get_new_password = GetNewPasswordInput(self.save_new_password)
        
        # Display add passwords frame
        add_passwords_frame.pack(fill = 'both', expand = TRUE)
        
    # Used to get inputs for new password and description
    def get_inputs(self):
        if path.exists('Saved_Passwords.txt'):
            with open('Saved_Passwords.txt', 'rb') as file:
                data = file.read()

            decrypt_data = use_key.decrypt(data)
            string_data = decrypt_data.decode()

            with open('Saved_Passwords.txt', 'w') as file:
                file.write(string_data)

        # Add starting divider using usernames to distinguish passwords
        saved_passwords = open('Saved_Passwords.txt', 'a')
        saved_passwords.write(self.read_username.get() + ' start')
        saved_passwords.write('\n')
        saved_passwords.close()
        
        # Used to get description and password
        self.get_new_password_description.new_description_input()
        self.get_new_password.new_password_input()

        # Add ending divider using usernames to distinguish passwords
        saved_passwords = open('Saved_Passwords.txt', 'a')
        saved_passwords.write(self.read_username.get() + ' end')
        saved_passwords.write('\n\n')
        saved_passwords.close()

        # Encrypt file with user data
        with open('Saved_Passwords.txt', 'rb') as read_file:
            data = read_file.read()

        encrypt_data = use_key.encrypt(data)

        with open('Saved_Passwords.txt', 'wb') as write_file:
            write_file.write(encrypt_data)
        
        # Close add passwords frame
        self.frame['add_passwords_frame'].destroy()

        # Return to the dashboard frame
        self.dashboard_frame()
        
        # Display a success message
        messagebox.showinfo(title = 'Success', message = 'Your password has been saved.')

    # Return to dashboard frame when back button is clicked
    def return_dashboard(self):
        self.dashboard_frame()
        
    # Close window when exit button is clicked
    def exit_window(self):
        self.window.destroy()

# Run the program
def main():
    x = tk.Tk()
    y = GUIMainWindow(x)
    z = GUIMainButtons(x)
    x.mainloop()
    
# Script checker
if __name__ == "__main__":
    main()

