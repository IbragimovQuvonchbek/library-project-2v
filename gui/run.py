import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
from tkinter import *
from tkinter import messagebox
import socket

from dotenv import load_dotenv

from scripts.functions import user_exists, signup, login, is_superuser, show_all_books, search_books, \
    get_registered_books, search_registered_books, get_book_by_id, is_book_registered, delete_book, add_book, \
    show_users, search_users, get_user_by_id, get_user_books_info, register_book, unregister_book, edit_book

load_dotenv()


def is_internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        messagebox.showerror("Connection Status", "No internet connection.")
    return False


class Intro:
    def __init__(self):
        self.window = Tk()
        self.window.title('Library')
        self.window.minsize(width=600, height=600)

        label_intro = Label(self.window, text='Library', font=("Arial", 34, "bold"))
        label_intro.place(relx=0.5, rely=0.4, anchor='center')

        signup_button = Button(self.window, text='Sign up', command=self.sign_up_command)
        signup_button.place(relx=0.3, rely=0.6, anchor='center')
        signup_button['font'] = ("Arial", 20)

        login_button = Button(self.window, text='Log in', command=self.log_in_command)
        login_button.place(relx=0.7, rely=0.6, anchor='center')
        login_button['font'] = ("Arial", 20)

        self.window.mainloop()

    def sign_up_command(self):
        if is_internet_available():
            self.window.destroy()
            SignUp()

    def log_in_command(self):
        if is_internet_available():
            self.window.destroy()
            LogIn()


class SignUp:
    code_verif = None

    def __init__(self):
        self.window = Tk()
        self.window.title("Library")
        self.window.minsize(width=600, height=600)

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.label_signup = Label(self.window, pady=50, padx=10)
        self.label_signup['text'] = 'Sign up'
        self.label_signup['font'] = ("Arial", 34, "bold")
        self.label_signup.grid(row=0, column=1)

        self.label_name = Label(self.window, text="name: ", font=('Arial', 20))
        self.label_name.grid(row=1, column=0)
        self.name = Entry(self.window, font=("Arial", 20))
        self.name.grid(row=1, column=1)

        self.label_surname = Label(self.window, text="surname: ", font=('Arial', 20), pady=10, padx=10)
        self.label_surname.grid(row=2, column=0)
        self.surname = Entry(self.window, font=("Arial", 20))
        self.surname.grid(row=2, column=1)

        self.label_username = Label(self.window, text="username: ", font=('Arial', 20), pady=10, padx=10)
        self.label_username.grid(row=3, column=0)
        self.username = Entry(self.window, font=("Arial", 20))
        self.username.grid(row=3, column=1)

        self.label_gmail = Label(self.window, text="gmail: ", font=('Arial', 20), pady=10, padx=10)
        self.label_gmail.grid(row=4, column=0)
        self.gmail = Entry(self.window, font=("Arial", 20))
        self.gmail.grid(row=4, column=1)

        self.label_password = Label(self.window, text="password: ", font=('Arial', 20), pady=10, padx=10)
        self.label_password.grid(row=5, column=0)
        self.password = Entry(self.window, font=("Arial", 20))
        self.password.grid(row=5, column=1)

        self.label_verif = Label(self.window, text="verification code: ", font=('Arial', 20), pady=10, padx=10)
        self.label_verif.grid(row=6, column=0)
        self.verif = Entry(self.window, font=("Arial", 20))
        self.verif.grid(row=6, column=1)

        self.label_check_gmail = Label(self.window, text="", font=('Arial', 14), pady=10, padx=10)
        self.label_check_gmail.grid(row=7, column=1)

        self.get_code_button = Button(self.window, text="get code", font=("Arial", 20), command=self.get_code)
        self.get_code_button.grid(row=8, column=0, pady=50, padx=10)

        self.register_button = Button(self.window, text="register", font=("Arial", 20), command=self.register_button)
        self.register_button.grid(row=8, column=1, pady=50, padx=10)

        self.window.mainloop()

    def go_back(self):
        self.window.destroy()
        Intro()

    def get_code(self):
        if is_internet_available():
            if not self.name.get() or not self.username.get() or not self.gmail.get() or not self.surname.get():
                messagebox.showwarning("WARNING", "Fill all empty spaces")
                return
            if user_exists(username=self.username.get(), gmail=self.gmail.get()):
                messagebox.showwarning("WARNING", 'gmail or username already exists')
                return
            try:
                self.send_verification()
            except (socket.gaierror, TimeoutError):
                messagebox.showwarning("WARNING", "Connection lost")
            except (smtplib.SMTPRecipientsRefused, smtplib.SMTPException):
                messagebox.showwarning("WARNING", "Make sure your gmail address is correct")

    def send_verification(self):
        verification_code = randint(100000, 999999)
        self.code_verif = verification_code
        sender = 'Library Manager'
        receiver = self.gmail.get()
        code = verification_code
        f_name = self.name.get()
        l_name = self.surname.get()
        subject = 'Library sign up verification'
        body = f'Hello {l_name} {f_name}, Your verification code - {code}'

        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        username = os.environ.get("GMAIL")
        password = os.environ.get("PASSWORD_GMAIL")

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)

        server.sendmail(sender, receiver, message.as_string())
        server.quit()
        self.label_check_gmail['fg'] = 'green'
        self.label_check_gmail['text'] = 'verification code sent to your gmail'

    def register_button(self):
        if is_internet_available():
            if str(self.code_verif) == str(self.verif.get()):
                is_registered = signup(name=self.name.get(), surname=self.surname.get(), gmail=self.gmail.get(),
                                       username=self.username.get(),
                                       password=self.password.get())
                if is_registered != -1:
                    self.window.destroy()
                    LogIn()
                else:
                    messagebox.showinfo("Username or gmail already exists", "Username or gmail already exists")
            else:
                messagebox.showerror("Incorrect verification code", "CODE ERROR")


class LogIn:
    def __init__(self):
        self.window = Tk()
        self.window.title("Library")
        self.user_id = -1
        self.window.minsize(width=600, height=600)
        self.superuser = ""
        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.label_signup = Label(self.window, pady=50, padx=10)
        self.label_signup['text'] = 'Log in'
        self.label_signup['font'] = ("Arial", 34, "bold")
        self.label_signup.grid(row=0, column=1)

        self.label_username = Label(self.window, text="username: ", font=('Arial', 20), pady=10, padx=10)
        self.label_username.grid(row=1, column=0)
        self.username = Entry(self.window, font=("Arial", 20))
        self.username.grid(row=1, column=1)

        self.label_password = Label(self.window, text="password: ", font=('Arial', 20), pady=10, padx=10)
        self.label_password.grid(row=2, column=0)
        self.password = Entry(self.window, font=("Arial", 20))
        self.password.grid(row=2, column=1)

        self.login_button = Button(self.window, text="log in", font=("Arial", 20), command=self.login)
        self.login_button.grid(row=3, column=1, pady=50, padx=10)

        self.window.mainloop()

    def go_back(self):
        self.window.destroy()
        Intro()

    def login(self):
        if is_internet_available():
            self.superuser = self.username.get()
            is_registered = login(username=self.username.get(), password=self.password.get())
            self.user_id = is_registered
            if is_registered != -1:
                self.window.destroy()
                Home(is_superuser(self.user_id), self.user_id)
            else:
                messagebox.showerror("Incorrect username or password", "Incorrect username or password")


class Home:
    def __init__(self, superuser, user_id):
        self.window = Tk()
        self.superuser = superuser
        self.user_id = user_id
        self.window.minsize(width=600, height=600)
        self.window.title("Library")
        self.x = 0
        self.y = 0

        if self.superuser:
            self.add_books_button = Button(self.window, text="add books", font=("Arial", 20), padx=self.x,
                                           pady=self.y, command=self.add_book_command)
            self.add_books_button.grid(row=0, column=0)
            self.clients_button = Button(self.window, text="see users", font=("Arial", 20), padx=self.x,
                                         pady=self.y, command=self.clients_button_command)
            self.clients_button.grid(row=0, column=1)
        else:
            self.x = 4
            self.y = 4

        self.see_books_button = Button(self.window, text="see books", font=("Arial", 20), padx=self.x, pady=self.y,
                                       command=self.see_books_command)
        self.see_books_button.grid(row=0, column=2)

        if not self.superuser:
            self.registered_books_button = Button(self.window, text="registered books", font=("Arial", 20), padx=self.x,
                                                  pady=self.y, command=self.registered_books)
            self.registered_books_button.grid(row=0, column=3)

        self.log_out_button = Button(self.window, text="log out", font=("Arial", 20), padx=self.x, pady=self.y,
                                     command=self.log_out_command)
        self.log_out_button.grid(row=0, column=4)

        self.window.mainloop()

    def add_book_command(self):
        if is_internet_available():
            self.window.destroy()
            AddBook(superuser=self.superuser, user_id=self)

    def log_out_command(self):
        if is_internet_available():
            self.window.destroy()
            Intro()

    def clients_button_command(self):
        if is_internet_available():
            self.window.destroy()
            SeeUsers(superuser=self.superuser, user_id=self.user_id)

    def see_books_command(self):
        if is_internet_available():
            self.window.destroy()
            SeeBooks(user_id=self.user_id, superuser=self.superuser)

    def registered_books(self):
        if is_internet_available():
            self.window.destroy()
            RegisteredBooks(user_id=self.user_id, superuser=self.superuser)


class SeeBooks:
    def __init__(self, superuser, user_id):
        self.window = Tk()
        self.superuser = superuser
        self.user_id = user_id
        self.window.minsize(width=600, height=600)
        self.window.title("Library")

        self.all_books = show_all_books()

        self.listbox = Listbox(self.window, font=("Arial", 20))
        self.listbox.grid(row=1, column=1, sticky="nsew")

        scrollbar = Scrollbar(self.window, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)

        for item in self.all_books:
            self.listbox.insert(END, f'{item[0]}. {item[1]}')

        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.search_entry = Entry(font=("Arial", 20))
        self.search_entry.grid(row=2, column=1, )

        self.search_button = Button(text="search", font=("Arial", 12), pady=5, padx=10,
                                    command=self.search_button_command)
        self.search_button.grid(column=3, row=2)

        self.window.mainloop()

    def search_button_command(self):
        if is_internet_available():
            keyword = self.search_entry.get()
            if keyword:
                data = search_books(keyword)
                self.listbox.delete(0, END)
                for item in data:
                    self.listbox.insert(END, f'{item[0]}. {item[1]}')
            else:
                data = show_all_books()
                self.listbox.delete(0, END)
                for item in data:
                    self.listbox.insert(END, f'{item[0]}. {item[1]}')

    def go_back(self):
        if is_internet_available():
            self.window.destroy()
            Home(superuser=self.superuser, user_id=self.user_id)

    def on_select(self, event):
        if is_internet_available():
            selected_item = self.listbox.get(self.listbox.curselection())
            return selected_item

    def on_double_click(self, event):
        if is_internet_available():
            book_id = int(str(self.listbox.get(self.listbox.curselection())).split('.')[0])
            self.window.destroy()
            SpecificBook(user_id=self.user_id, superuser=self.superuser, book_id=book_id, current_window="SeeBooks")


class RegisteredBooks:
    def __init__(self, user_id, superuser):
        self.window = Tk()
        self.window.minsize(width=600, height=600)
        self.window.title("Library")

        self.user_id = user_id
        self.superuser = superuser

        self.all_books = get_registered_books(self.user_id)

        self.listbox = Listbox(self.window, font=("Arial", 20))
        self.listbox.grid(row=1, column=1, sticky="nsew")

        scrollbar = Scrollbar(self.window, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)

        for item in self.all_books:
            self.listbox.insert(END, f'{item[0]}. {item[1]}')

        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.search_entry = Entry(font=("Arial", 20))
        self.search_entry.grid(row=2, column=1, )

        self.search_button = Button(text="search", font=("Arial", 12), pady=5, padx=10,
                                    command=self.search_button_command)
        self.search_button.grid(column=3, row=2)

        self.window.mainloop()

    def search_button_command(self):
        if is_internet_available():
            keyword = self.search_entry.get()
            if keyword:
                data = search_registered_books(keyword, self.all_books)
                self.listbox.delete(0, END)
                for item in data:
                    self.listbox.insert(END, f'{item[0]}. {item[1]}')

    def go_back(self):
        self.window.destroy()
        Home(superuser=self.superuser, user_id=self.user_id)

    def on_select(self, event):
        if is_internet_available():
            selected_item = self.listbox.get(self.listbox.curselection())
            return selected_item

    def on_double_click(self, event):
        if is_internet_available():
            book_id = int(str(self.listbox.get(self.listbox.curselection())).split('.')[0])
            self.window.destroy()
            SpecificBook(user_id=self.user_id, superuser=self.superuser, book_id=book_id,
                         current_window="RegisteredBooks")


def go_back(self):
    self.window.destroy()
    SeeBooks(superuser=self.superuser, user_id=self.user_id)


class SpecificBook:
    def __init__(self, user_id, superuser, book_id, current_window):
        self.window = Tk()
        self.window.minsize(width=600, height=600)
        self.window.title("Library")

        self.user_id = user_id
        self.superuser = superuser
        self.book_id = book_id
        self.current_window = current_window

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.book_info = get_book_by_id(self.book_id)
        book_to_str = f'''
        Name: {self.book_info[1]}
        Author: {self.book_info[2]}
        Category: {self.book_info[3]}
        Description: {self.book_info[4]}
        Unit: {self.book_info[5]}
        '''

        self.book_label = Label(self.window, text=book_to_str, font=("Roboto", 16), justify='left')
        self.book_label.grid(row=1, column=2)

        if not self.superuser:
            self.register_info_label = Label(text="", font=("Arial", 15), fg="green")
            self.register_info_label.grid(row=2, column=1)

            self.is_registered = is_book_registered(book_id=self.book_id, user_id=self.user_id)

            self.button_text = "unregister" if self.is_registered else "register"

            self.register_button = Button(text=self.button_text, font=("Arial", 15),
                                          command=self.register_button_command)
            self.register_button.grid(row=3, column=1)

        else:
            self.register_button = Button(text="edit", font=("Arial", 15),
                                          command=self.edit_button_command)
            self.register_button.grid(row=3, column=0)

            self.register_button = Button(text="delete", font=("Arial", 15),
                                          command=self.delete_button_command)
            self.register_button.grid(row=3, column=1)

        self.window.mainloop()

    def edit_button_command(self):
        if is_internet_available():
            self.window.destroy()
            EditBook(superuser=self.superuser, user_id=self.user_id, book_id=self.book_id)

    def delete_button_command(self):
        if is_internet_available():
            delete_book(self.book_id)
            self.window.destroy()
            Home(superuser=self.superuser, user_id=self.user_id)

    def go_back(self):
        self.window.destroy()
        if self.current_window == "SeeBooks":
            SeeBooks(superuser=self.superuser, user_id=self.user_id)
        elif self.current_window == "RegisteredBooks":
            RegisteredBooks(superuser=self.superuser, user_id=self.user_id)
        elif self.current_window == "AddBook":
            Home(superuser=self.superuser, user_id=self.user_id)
        else:
            Home(superuser=self.superuser, user_id=self.user_id)

    def register_button_command(self):
        if is_internet_available():
            if self.is_registered:
                unregister_book(book_id=self.book_id, user_id=self.user_id)
                self.button_text = "unregister" if self.is_registered else "register"
                self.register_info_label['text'] = f"book is {self.button_text}ed"
                self.is_registered = is_book_registered(book_id=self.book_id, user_id=self.user_id)
                self.button_text = "unregister" if self.is_registered else "register"
                self.register_button['text'] = self.button_text
            else:
                register_book(book_id=self.book_id, user_id=self.user_id)
                self.button_text = "unregister" if self.is_registered else "register"
                self.register_info_label['text'] = f"book is {self.button_text}ed"
                self.is_registered = is_book_registered(book_id=self.book_id, user_id=self.user_id)
                self.button_text = "unregister" if self.is_registered else "register"
                self.register_button['text'] = self.button_text


class AddBook:
    def __init__(self, superuser, user_id):
        self.window = Tk()
        self.window.title("Library")
        self.window.minsize(width=600, height=600)

        self.superuser = superuser
        self.user_id = user_id

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.label_name = Label(self.window, text="name: ", font=('Arial', 20), padx=10, pady=10)
        self.label_name.grid(row=1, column=0)
        self.name = Entry(self.window, font=("Arial", 20))
        self.name.grid(row=1, column=1)

        self.label_author = Label(self.window, text="author: ", font=('Arial', 20), padx=10, pady=10)
        self.label_author.grid(row=2, column=0)
        self.author = Entry(self.window, font=("Arial", 20))
        self.author.grid(row=2, column=1)

        self.label_category = Label(self.window, text="category: ", font=('Arial', 20), padx=10, pady=10)
        self.label_category.grid(row=3, column=0)
        self.category = Entry(self.window, font=("Arial", 20))
        self.category.grid(row=3, column=1)

        self.label_description = Label(self.window, text="description: ", font=('Arial', 20), padx=10, pady=10)
        self.label_description.grid(row=4, column=0)
        self.description = Entry(self.window, font=("Arial", 20))
        self.description.grid(row=4, column=1)

        self.unit_description = Label(self.window, text="unit: ", font=('Arial', 20), padx=10, pady=10)
        self.unit_description.grid(row=5, column=0)
        self.unit = Entry(self.window, font=("Arial", 20))
        self.unit.grid(row=5, column=1)

        self.add_button = Button(text="add book", font=('Arial', 20), command=self.add_button_command)
        self.add_button.grid(row=6, column=1)

        self.window.mainloop()

    def go_back(self):
        self.window.destroy()
        Home(superuser=self.superuser, user_id=self.user_id)

    def add_button_command(self):
        if is_internet_available():
            book_id = add_book(name=self.name.get(), author=self.author.get(), category=self.category.get(),
                               description=self.description.get(), unit=self.unit.get())
            self.window.destroy()
            SpecificBook(user_id=self.user_id, superuser=self.superuser, book_id=book_id, current_window="AddBook")


class EditBook:
    def __init__(self, superuser, user_id, book_id):
        self.window = Tk()
        self.window.title("Library")
        self.window.minsize(width=600, height=600)

        self.superuser = superuser
        self.user_id = user_id
        self.book_id = book_id

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.label_name = Label(self.window, text="name: ", font=('Arial', 20), padx=10, pady=10)
        self.label_name.grid(row=1, column=0)
        self.name = PlaceholderEntry(self.window, placeholder="leave it for unchanged", font=("Arial", 20))
        self.name.grid(row=1, column=1)

        self.label_author = Label(self.window, text="author: ", font=('Arial', 20), padx=10, pady=10)
        self.label_author.grid(row=2, column=0)
        self.author = PlaceholderEntry(self.window, placeholder="leave it for unchanged", font=("Arial", 20))
        self.author.grid(row=2, column=1)

        self.label_category = Label(self.window, text="category: ", font=('Arial', 20), padx=10, pady=10)
        self.label_category.grid(row=3, column=0)
        self.category = PlaceholderEntry(self.window, placeholder="leave it for unchanged", font=("Arial", 20))
        self.category.grid(row=3, column=1)

        self.label_description = Label(self.window, text="description: ", font=('Arial', 20), padx=10, pady=10)
        self.label_description.grid(row=4, column=0)
        self.description = PlaceholderEntry(self.window, placeholder="leave it for unchanged", font=("Arial", 20))
        self.description.grid(row=4, column=1)

        self.label_unit = Label(self.window, text="unit: ", font=('Arial', 20), padx=10, pady=10)
        self.label_unit.grid(row=5, column=0)
        self.unit = PlaceholderEntry(self.window, placeholder="leave it for unchanged", font=("Arial", 20))
        self.unit.grid(row=5, column=1)

        self.edit_button = Button(text="edit book", font=('Arial', 20), command=self.edit_button_command)
        self.edit_button.grid(row=6, column=1)

        self.window.mainloop()

    def go_back(self):
        self.window.destroy()
        Home(superuser=self.superuser, user_id=self.user_id)

    def edit_button_command(self):
        if is_internet_available():
            edit_book(name=self.name.get(), author=self.author.get(), category=self.category.get(),
                      description=self.description.get(), book_id=self.book_id, unit=self.unit.get())
            self.window.destroy()
            SpecificBook(superuser=self.superuser, user_id=self.user_id, book_id=self.book_id,
                         current_window="EditBook")


class PlaceholderEntry(Entry):
    def __init__(self, master=None, placeholder="", color='red', *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.on_entry_focus)
        self.bind("<FocusOut>", self.on_entry_focus_out)

    def on_entry_focus(self, event):
        if self.get() == self.placeholder:
            self.delete(0, END)
            self.config(fg=self.default_fg_color)

    def on_entry_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)


class SeeUsers:
    def __init__(self, superuser, user_id):
        self.window = Tk()
        self.superuser = superuser
        self.user_id = user_id
        self.window.minsize(width=600, height=600)
        self.window.title("Library")

        self.all_users = show_users()

        self.listbox = Listbox(self.window, font=("Arial", 20))
        self.listbox.grid(row=1, column=1, sticky="nsew")

        scrollbar = Scrollbar(self.window, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)

        for item in self.all_users:
            self.listbox.insert(END, f'{item[0]}. {item[1]}')

        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.search_entry = Entry(font=("Arial", 20))
        self.search_entry.grid(row=2, column=1, )

        self.search_button = Button(text="search", font=("Arial", 12), pady=5, padx=10,
                                    command=self.search_button_command)
        self.search_button.grid(column=3, row=2)

        self.window.mainloop()

    def search_button_command(self):
        if is_internet_available():
            keyword = self.search_entry.get()
            if keyword.strip():
                data = search_users(keyword)
                self.listbox.delete(0, END)
                for item in data:
                    self.listbox.insert(END, f'{item[0]}. {item[1]}')
            else:
                data = show_users()
                self.listbox.delete(0, END)
                for item in data:
                    self.listbox.insert(END, f'{item[0]}. {item[1]}')

    def go_back(self):
        self.window.destroy()
        Home(superuser=self.superuser, user_id=self.user_id)

    def on_select(self, event):
        if is_internet_available():
            selected_item = self.listbox.get(self.listbox.curselection())
            return selected_item

    def on_double_click(self, event):
        if is_internet_available():
            user_id = int(str(self.listbox.get(self.listbox.curselection())).split('.')[0])
            self.window.destroy()
            SpecificUser(user_id=self.user_id, superuser=self.superuser, current_user=user_id)


class SpecificUser:
    def __init__(self, user_id, superuser, current_user):
        self.window = Tk()
        self.window.minsize(width=600, height=600)
        self.window.title("Library")

        self.user_id = user_id
        self.superuser = superuser
        self.current_user = current_user

        self.back_button = Button(text="⬅️", font=18, padx=5, pady=5, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        self.client_info = get_user_by_id(self.current_user)
        book_to_str = f'''
        Id: {self.client_info[0]}
        Name: {self.client_info[1]}
        Surname: {self.client_info[2]}
        Username: {self.client_info[3]}
        Gmail: {self.client_info[4]}
        Book:'''

        self.client_book_info = get_user_books_info(self.current_user)
        length_books_data = len(self.client_book_info)
        if length_books_data == 0:
            book_to_str += " no books"
        else:
            for index, book in enumerate(self.client_book_info):
                if index % 3 == 0 and index != 0:
                    book_to_str += f"\n{book[0]}, "
                else:
                    book_to_str += f"{book[0]}, "

        self.book_label = Label(self.window, text=book_to_str, font=("Roboto", 16), justify='left')
        self.book_label.grid(row=1, column=2)

        self.window.mainloop()

    def go_back(self):
        self.window.destroy()
        Home(superuser=self.superuser, user_id=self.user_id)


Intro()
