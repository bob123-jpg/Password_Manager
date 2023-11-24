'''
Author: Matthew Cao

Date: November 14, 2023

Description: This program is a password manager desktop application designed to securely store passwords. Methods like
encryption, security keys, and clipboard cleaning are utilized to secure passwords.

Resources:
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
https://www.w3schools.com/python/python_file_remove.asp
https://stackoverflow.com/questions/53226110/how-to-clear-clipboard-in-using-python
https://www.tutorialspoint.com/how-to-change-the-background-color-of-a-tkinter-canvas-dynamically
https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
https://www.tutorialspoint.com/python/tk_text.htm
https://www.tutorialspoint.com/how-to-center-a-window-on-the-screen-in-tkinter#:~:text=In%20order%20to%20place%20a,programmatically%20by%20defining%20its%20geometry.
https://www.geeksforgeeks.org/convert-python-script-to-exe-file/
https://chat.openai.com/
'''

# Import libraries
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
import re
import cryptography
from cryptography.fernet import Fernet
import os.path
from os import path
import pyperclip

# Set up a key file for encrypting and decrypting files
if not path.exists('Key.key'):
    key = Fernet.generate_key()

    with open('Key.key', 'wb') as file:
        file.write(key)

with open('Key.key', 'rb') as file:
    key = file.read()

use_key = Fernet(key)
    
'''Classes for main window of user interface'''
# Set up layout of window
class GUIMainWindow:
    def __init__(self, window):
        self.window = window

        # Background color for window
        background = Canvas(window, bg = 'gray90').pack()
        
        # Title for window
        self.window.title('Main Menu')

        # Initialize window size
        self.window.geometry('350x270')

        # Prevent window from being resized
        self.window.resizable(width = False, height = False)

        # Center window on screen
        self.window.eval('tk::PlaceWindow . center')

        # Labels within window
        header = Label(window, text = 'Password Manager', bg = 'gray90', fg = 'blue4', \
            font = ('Times New Roman underline', 24)).place(relx = .5, rely = .1, anchor = CENTER)
        
# Buttons within window
class GUIMainButtons:
    def __init__(self, buttons):
        self.buttons = buttons
        # Button for new users
        new_user = Button(buttons, text = 'New User', bd = '3', width = 10, height = 2, bg = 'gray87', \
            font = ('Times New Roman', 14), command = self.new_user_window).place(x = 40, y = 80)
        
        # Button for returning users
        returning_user = Button(buttons, text = 'Returning\nUser', bd = '3', width = 10, height = 2, bg = 'gray87', \
            font = ('Times New Roman', 14), command = self.returning_user_window).place(x = 200, y = 80)

        # Button to view usage information
        info = Button(buttons, text = 'Info', bd = '3', width = 10, height = 2, bg = 'gray75', \
            font = ('Times New Roman', 14), command = self.info_window).place(x = 40, y = 180)
        
        # Button to exit
        exit = Button(buttons, text = 'Exit', bd = '3', width = 10, height = 2, bg = 'coral', \
            font = ('Times New Roman', 14), command = self.exit_window).place(x = 200, y = 180)
        
    # Open new user window when New User button is clicked
    def new_user_window(self):
        new_user_window_toplevel = Toplevel(self.buttons.winfo_toplevel())
        GUINewUserWindow(new_user_window_toplevel)
        self.buttons.iconify()

    # Open returning user window when Returning User button is clicked
    def returning_user_window(self):
        returning_user_window_toplevel = Toplevel(self.buttons.winfo_toplevel())
        GUIReturningUserWindow(returning_user_window_toplevel)
        self.buttons.iconify()
        
    # Open usage information window when Info button is clicked
    def info_window(self):
        info_window_toplevel = Toplevel(self.buttons.winfo_toplevel())
        GUIInfoWindow(info_window_toplevel)
        self.buttons.iconify()
    
    # Close window when Exit button is clicked
    def exit_window(self):
        self.buttons.destroy()
        
'''Classes for saving user inputs'''  
# Save and manipulate username input
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
        
'''Class for a window opened by clicking New User button'''
# Open a new window when New User button is clicked in main window
class GUINewUserWindow:
    def __init__(self, window):
        self.window = window
        
        # Used to save user inputs
        self.save_username = StringVar()
        self.save_password = StringVar()
        
        # Title for window
        self.window.title('New User')
        
        # Set size of window
        self.window.geometry('500x300')
        
        # Prevent window from being resized
        self.window.resizable(width = False, height = False)
        
        # Background color for window
        background = Canvas(window, bg = 'gray90').pack()

        # Header label
        header = Label(window, text = 'Register an account', bg = 'gray90', fg = 'blue4', font = ('Times New Roman', 18)) \
            .place(relx = .5, rely = .1, anchor = CENTER)
        
        # Username label and entry
        username_label = Label(window, text = 'Username:', bg = 'gray90', font = ('Times New Roman', 12)).place(x = 100, y = 100)
        username_entry = Entry(window, bd = 3, font = ('Times New Roman', 12), textvariable = self.save_username).place(x = 230, y = 100)
        # Password label and entry
        password_label = Label(window, text = 'Password:', bg = 'gray90', font = ('Times New Roman', 12)).place(x = 100, y = 150)
        password_entry = Entry(window, bd = 3, font = ('Times New Roman', 12), textvariable = self.save_password, show = '*').place(x = 230, y = 150)

        # Button to complete new user account creation
        save_profile = Button(window, text = 'Sign Up', bd = '3', width = 7, height = 1, bg = 'gray90', \
            font = ('Times New Roman', 12), command = self.get_inputs).place(relx = .5, rely = .85, anchor = CENTER)

        # Call classes to save inputs to file
        self.get_username = GetUsernameInput(self.save_username)
        self.get_password = GetPasswordInput(self.save_password)
        
    # Function to help save inputs to file and perform input validation
    def get_inputs(self):
        # Array of special characters for password input validation
        password_symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        # Get user inputs for input validation
        check_username = self.save_username.get()
        check_password = self.save_password.get()
        
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
            for char in check_password) or not any(char in password_symbols for char in check_password):
            messagebox.showerror(title = 'Error', message = 'Password must contain a number, uppercase letter, \nlowercase letter, \
                special symbol (e.g., !@#$), and \nbe at least 12 characters long. Please try again.')
        else:
            # Get all user inputs
            self.get_username.username_input()
            self.get_password.password_input()

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
class GUIReturningUserWindow:
    def __init__(self, window):
        self.window = window
        
        # Used to read user inputs
        self.read_username = StringVar()
        self.read_password = StringVar()
        
        # Title for window
        self.window.title('Returning User')
        
        # Set size of window
        self.window.geometry('500x300')
        
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

        # Background color for frame
        background = Canvas(login_frame, bg = 'gray90').pack()
            
        # Header label
        header = Label(login_frame, bg = 'gray90', fg = 'blue4', text = 'Log in to manage your passwords',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)

        # Username label and entry
        username_label = Label(login_frame, bg = 'gray90', text = 'Username:', font = ('Times New Roman', 12)).place(x = 100, y = 100)
        username_entry = Entry(login_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.read_username).place(x = 230, y = 100)
        # Password label and entry
        password_label = Label(login_frame, bg = 'gray90', text = 'Password:', font = ('Times New Roman', 12)).place(x = 100, y = 150)
        password_entry = Entry(login_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.read_password, show = '*').place(x = 230, y = 150)
        
        # Button to complete login
        login = Button(login_frame, text = 'Login', bd = '3', width = 7, height = 1, font = ('Times New Roman', 12), \
            command  = self.check_close_login_frame).place(relx = .5, rely = .85, anchor = CENTER)

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

    # Frame to display a dashboard
    def dashboard_frame(self):
        dashboard_frame = Frame(self.window)
        self.frame['dashboard_frame'] = dashboard_frame

        # Background color for frame
        background = Canvas(dashboard_frame, bg = 'gray90').pack()
        
        # Header label
        header = Label(dashboard_frame, bg = 'gray90', fg = 'blue4', text = 'Select an option below',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)
        
        # Button to view passwords
        view_passwords = Button(self.window, text = 'View\nPasswords', bd = '3', width = 10, height = 2, \
            font = ('Times New Roman', 14), command = self.view_passwords_frame).place(x = 120, y = 100)

        # Button to add passwords
        add_passwords = Button(self.window, text = 'Add\nPasswords', bd = '3', width = 10, \
            height = 2, font = ('Times New Roman', 14), command = self.add_passwords_frame).place(x = 270, y = 100)
        
        # Button to exit
        exit = Button(self.window, text = 'Exit', bd = '3', width = 7, height = 1, \
            font = ('Times New Roman', 12), command = self.exit_window).place(relx = .5, rely = .85, anchor = CENTER)
        
        # Display multi-authentication frame
        dashboard_frame.pack(fill = 'both', expand = TRUE)

    # Frame for user to view saved passwords
    def view_passwords_frame(self):
        # Close dashboard frame
        self.frame['dashboard_frame'].destroy()
        
        # Set up view passwords frame
        view_passwords_frame = Frame(self.window)
        self.frame['view_passwords_frame'] = view_passwords_frame

        # Background color for frame
        background = Canvas(view_passwords_frame, bg = 'gray90').pack()
        
        # Header label
        header = Label(view_passwords_frame, bg = 'gray90', fg = 'blue4', text = 'Your saved passwords:',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)

        # Set up text and scrollbar widgets to display passwords
        text = Text(view_passwords_frame)
        text.pack(fill = BOTH)
        text.place(x = 61, y = 50, width = 378, height = 170)
        scroll = Scrollbar(text)
        scroll.config(command = text.yview)
        text.config(yscrollcommand = scroll.set)
        scroll.pack(side = RIGHT, fill = Y)
        
        try:
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
            
        except FileNotFoundError:
            pass
        
        # Button to return to dashboard frame
        back = Button(view_passwords_frame, text = 'Back', bd = '3', width = 10, height = 2, font = ('Times New Roman', 12), \
            command = lambda: [self.dashboard_frame(), self.frame['view_passwords_frame'].destroy()]).place(relx = .35, rely = .87, anchor = CENTER)

        # Button to remove passwords
        remove = Button(view_passwords_frame, text = 'Remove\nPassword', bd = '3', width = 10, height = 2, font = ('Times New Roman', 12), \
            command = self.remove_password).place(relx = .65, rely = .87, anchor = CENTER)
        
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

        # Format decrypted data
        format_data = string_data.split('\n')

        # Find password to remove and associated data
        for i, j in enumerate(format_data):
            if 'Password: {}'.format(remove_message) in j:
                for k in range(i, -1, -1):
                    if 'start' in format_data[k]:
                        start_data = k
                        break
                for m in range(i, len(format_data)):
                    if 'end' in format_data[m]:
                        end_data = m
                        break
            
        # Remove password and associated data
        del format_data[start_data:end_data]

        # Encrypt data and write back to file
        new_data = '\n'.join(format_data)
        save_data = new_data.encode()
        encrypted_data = use_key.encrypt(save_data)

        with open('Saved_Passwords.txt', 'wb') as file:
            file.write(encrypted_data)

    # Frame for user to add new passwords
    def add_passwords_frame(self):
        # Close dashboard frame
        self.frame['dashboard_frame'].destroy()
        
        # Set up add passwords frame
        add_passwords_frame = Frame(self.window)
        self.frame['add_passwords_frame'] = add_passwords_frame

        # Background color for frame
        background = Canvas(add_passwords_frame, bg = 'gray90').pack()

        # Header label
        header = Label(add_passwords_frame, bg = 'gray90', fg = 'blue4', text = 'Add a new password',\
            font = ('Times New Roman', 18)).place(relx = .5, rely = .1, anchor = CENTER)
        
        # New password description label and entry
        new_password_description_label = Label(add_passwords_frame, bg = 'gray90', text = 'Description\n(e.g., YouTube account):', \
            font = ('Times New Roman', 12)).place(x = 70, y = 100)
        new_password_description_entry = Entry(add_passwords_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_new_password_description).place(x = 250, y = 100)

        # Adding new password label and entry
        new_password_label = Label(add_passwords_frame, bg = 'gray90', text = 'Password:', font = ('Times New Roman', 12)).place(x = 112, y = 170)
        new_password_entry = Entry(add_passwords_frame, bd = 3, font = ('Times New Roman', 12), \
            textvariable = self.save_new_password).place(x = 250, y = 170)

        # Button to return to dashboard frame
        back = Button(add_passwords_frame, text = 'Back', bd = '3', width = 7, height = 1, font = ('Times New Roman', 12), \
            command = lambda: [self.dashboard_frame(), self.frame['add_passwords_frame'].destroy()]).place(x = 140, y = 240)
        
        # Button to finish adding new password
        finish_new_password = Button(add_passwords_frame, text = 'Save Password', bd = '3', width = 11, height = 1, \
            font = ('Times New Roman', 12), command = self.get_inputs).place(x = 250, y = 240)

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

'''Class to provide information to new users'''
# Show information for using application
class GUIInfoWindow:
    def __init__(self, window):
        self.window = window
        # Title for window
        self.window.title('Usage Information')
        # Set size of window
        self.window.geometry('700x350')
        # Prevent window from being resized
        self.window.resizable(width = False, height = False)
        # Call show_info function
        self.show_info()

        # Background color for window
        background = Canvas(window, bg = 'gray90').pack()

    # Window to display usage information
    def show_info(self):
        info_header = Label(self.window, text = 'Important Note', fg = 'red', font = ('Times New Roman underline', 18), pady = 30).pack()
        info_1 = Label(self.window, text = '- After running the application for the first time, a file called "Key.key" will be created', \
            font = ('Times New Roman', 14), justify = LEFT).pack()
        info_2 = Label(self.window, text = '- Move the file to a separate storage device and always use this key', \
            font = ('Times New Roman', 14), justify = LEFT).pack()
        info_3 = Label(self.window, text = '- Before starting the password manager, copy the key to the application\'s directory', \
            font = ('Times New Roman', 14), justify = LEFT).pack()
        info_4 = Label(self.window, text = '- It is recommended to make multiple copies of the key to prevent loss', \
            font = ('Times New Roman', 14), justify = LEFT).pack()
        info_5 = Label(self.window, text = '- If the key is lost, saved passwords will no longer be accessible', \
            font = ('Times New Roman', 14), justify = LEFT).pack()
        info_6 = Label(self.window, text = '- After closing the application, a copied password will be removed from your clipboard', \
            font = ('Times New Roman', 14), justify = LEFT).pack()

        # Button to exit window
        exit = Button(self.window, text = "Exit", bd = '3', width = 10, height = 1, font = ('Times New Roman', 14), \
            command = self.window.destroy).pack(pady = 30)

# Run the program
def main():
    x = tk.Tk()
    y = GUIMainWindow(x)
    z = GUIMainButtons(x)
    x.mainloop()

    # When program ends, remove decryption key to protected encrypted files
    os.remove('Key.key')

    # When program ends, clear clipboard to remove any copied passwords
    pyperclip.copy(' ')
    
# Script checker
if __name__ == "__main__":
    main()
