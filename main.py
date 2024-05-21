import pickle
import os
from collections import UserDict
from datetime import datetime
import re

# Helper functions for saving and loading data
def save_data(book, filename):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

# Field classes
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must contain 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Address(Field):
    pass

class Email(Field):
    def __init__(self, value):
        if "@" not in value or "." not in value.split("@")[1]:
            raise ValueError("Invalid email address")
        super().__init__(value)

# Record classes
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value if self.birthday else "N/A"
        address = self.address.value if self.address else "N/A"
        email = self.email.value if self.email else "N/A"
        return (f"Contact name: {self.name.value}, phones: {phones}, "
                f"birthday: {birthday}, address: {address}, email: {email}")

# Address Book
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                if (birthday_date - today).days <= days:
                    upcoming_birthdays.append((record.name.value, birthday_date))
        return upcoming_birthdays

# Note classes
class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []

    def add_tag(self, tag):
        self.tags.append(tag)

    def edit(self, new_content):
        self.content = new_content

    def __str__(self):
        tags = ", ".join(self.tags)
        return f"Title: {self.title}, Content: {self.content}, Tags: {tags}"

class NoteBook(UserDict):
    def add_note(self, note):
        self.data[note.title] = note

    def find(self, title):
        return self.data.get(title)

    def delete(self, title):
        if title in self.data:
            del self.data[title]

    def search_by_tag(self, tag):
        return [note for note in self.data.values() if tag in note.tags]

# Command handling functions
def parse_input(user_input):
    return user_input.split(maxsplit=2)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book):
    name, phone, *rest = args
    address = rest[0] if len(rest) > 0 else None
    email = rest[1] if len(rest) > 1 else None
    birthday = rest[2] if len(rest) > 2 else None
    record = book.find(name)
    if record:
        record.add_phone(phone)
        if address:
            record.add_address(address)
        if email:
            record.add_email(email)
        if birthday:
            record.add_birthday(birthday)
    else:
        record = Record(name)
        record.add_phone(phone)
        if address:
            record.add_address(address)
        if email:
            record.add_email(email)
        if birthday:
            record.add_birthday(birthday)
        book.add_record(record)
    return "Contact added."

@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    else:
        return f"Contact {name} not found."

@input_error
def show_phones(args, book):
    name, = args
    record = book.find(name)
    if record:
        phones = "; ".join(p.value for p in record.phones)
        return f"Phones for {name}: {phones}"
    else:
        return f"Contact {name} not found."

@input_error
def show_all_contacts(book):
    return "\n".join(str(record) for record in book.data.values())

@input_error
def delete_contact(args, book):
    name, = args
    book.delete(name)
    return f"Contact {name} deleted."

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return f"{record.name.value}: {record.birthday.value}"
    else:
        return f"No birthday found for {name}."

@input_error
def birthdays(args, book):
    days = int(args[0])
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if upcoming_birthdays:
        return "\n".join([f"{name}: {birthday}" for name, birthday in upcoming_birthdays])
    else:
        return "No upcoming birthdays found."

# Note handling functions
@input_error
def add_note(args, notebook):
    title, content = args
    note = Note(title, content)
    notebook.add_note(note)
    return f"Note '{title}' added."

@input_error
def find_note(args, notebook):
    title, = args
    note = notebook.find(title)
    if note:
        return str(note)
    else:
        return f"Note '{title}' not found."

@input_error
def edit_note(args, notebook):
    title, new_content = args
    note = notebook.find(title)
    if note:
        note.edit(new_content)
        return f"Note '{title}' updated."
    else:
        return f"Note '{title}' not found."

@input_error
def delete_note(args, notebook):
    title, = args
    notebook.delete(title)
    return f"Note '{title}' deleted."

@input_error
def add_tag(args, notebook):
    title, tag = args
    note = notebook.find(title)
    if note:
        note.add_tag(tag)
        return f"Tag '{tag}' added to note '{title}'."
    else:
        return f"Note '{title}' not found."

@input_error
def search_by_tag(args, notebook):
    tag, = args
    notes = notebook.search_by_tag(tag)
    if notes:
        return "\n".join(str(note) for note in notes)
    else:
        return f"No notes found with tag '{tag}'."

def guess_command(user_input, commands):
    for command in commands:
        if command in user_input:
            return command
    return "Invalid command."

def main():
    # Set up file paths for saving data
    user_folder = os.path.expanduser("~")
    contact_file = os.path.join(user_folder, "addressbook.pkl")
    note_file = os.path.join(user_folder, "notebook.pkl")

    # Load data
    address_book = AddressBook(load_data(contact_file))
    note_book = NoteBook(load_data(note_file))

    commands = {
        "hello": lambda args: "How can I help you?",
        "add": add_contact,
        "change": change_phone,
        "phone": show_phones,
        "all": lambda args: show_all_contacts(address_book),
        "delete": delete_contact,
        "birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "add-note": add_note,
        "find-note": find_note,
        "edit-note": edit_note,
        "delete-note": delete_note,
        "add-tag": add_tag,
        "search-by-tag": search_by_tag
    }

    while True:
        user_input = input("Enter a command: ").strip().lower()
        if user_input in ["close", "exit", "good bye"]:
            print("Good bye!")
            save_data(address_book, contact_file)
            save_data(note_book, note_file)
            break
        command_name, *args = parse_input(user_input)
        command_name = guess_command(command_name, commands)
        if command_name in commands:
            print(commands[command_name](args, address_book if "note" not in command_name and "tag" not in command_name else note_book))
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()