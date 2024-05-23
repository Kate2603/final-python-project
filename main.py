import pickle
from datetime import datetime, date, timedelta

class Contact:
    def __init__(self, name, phone, address=None, email=None, birthday=None):
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email
        self.birthday = birthday

    def __str__(self):
        return f"{self.name}: Phone: {self.phone}, Address: {self.address}, Email: {self.email}, Birthday: {self.birthday}"

class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone, address=None, email=None, birthday=None):
        self.contacts[name] = Contact(name, phone, address, email, birthday)
        return f"Contact {name} added."

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            return f"Contact {name} deleted."
        return f"Contact {name} not found."

    def change_phone(self, name, phone):
        if name in self.contacts:
            self.contacts[name].phone = phone
            return f"Phone number for {name} updated."
        return f"Contact {name} not found."

    def show_phones(self, name):
        if name in self.contacts:
            return f"{self.contacts[name].name}: {self.contacts[name].phone}"
        return f"Contact {name} not found."

    def show_all_contacts(self):
        return "\n".join(str(contact) for contact in self.contacts.values())

    def add_birthday(self, name, birthday):
        if name in self.contacts:
            self.contacts[name].birthday = birthday
            return f"Birthday for {name} added."
        return f"Contact {name} not found."

    def birthdays(self, days):
        today = date.today()
        this_week = today + timedelta(days=days)
        upcoming_birthdays = []

        for name, contact in self.contacts.items():
            if contact.birthday:
                birthday_date = datetime.strptime(contact.birthday, '%d.%m.%Y').date()
                birthday_date = birthday_date.replace(year=today.year)
                if birthday_date < today:
                    birthday_date = birthday_date.replace(year=today.year + 1)
                if today <= birthday_date <= this_week:
                    upcoming_birthdays.append((name, birthday_date))

        if upcoming_birthdays:
            message = "Birthdays this week:\n"
            for name, birthday in upcoming_birthdays:
                message += f"{name}: {birthday.strftime('%Y-%m-%d')}\n"
        else:
            message = "There are no birthdays this week."
        return message
class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags or []

    def __str__(self):
        return f"{self.title}: {self.content} Tags: {', '.join(self.tags)}"

class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, title, content):
        self.notes.append(Note(title, content))
        return f"Note {title} added."

    def edit_note(self, title, new_content):
        for note in self.notes:
            if note.title == title:
                note.content = new_content
                return f"Note {title} updated."
        return f"Note {title} not found."
    
    def find_note(self, title):
        for note in self.notes:
            if note.title == title:
                return str(note)
        return f"Note '{title}' not found."
    
    def show_all_notes(self):
        if not self.notes:
            return "No notes available."
        return "\n".join(str(note) for note in self.notes)

    def delete_note(self, title):
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                return f"Note {title} deleted."
        return f"Note {title} not found."

    def add_tag(self, title, tag):
        for note in self.notes:
            if note.title == title:
                note.tags.append(tag)
                return f"Tag(s) added to {title}."
        return f"Note {title} not found."

    def search_by_tag(self, tag):
        tagged_notes = [note for note in self.notes if tag in note.tags]
        if not tagged_notes:
            return "No notes found with that tag."
        return "\n".join(str(note) for note in tagged_notes)

def parse_input(user_input):
    command_parts = user_input.split(' ', 1)
    command = command_parts[0]
    args = command_parts[1].split(' ') if len(command_parts) > 1 else []
    return command, args

def load_data():
    try:
        with open('address_book.pkl', 'rb') as f:
            address_book = pickle.load(f)
            print("Address book data deserialized.")
    except FileNotFoundError:
        address_book = AddressBook()
        print("Address book not found. Created a new one.")

    try:
        with open('notebook.pkl', 'rb') as f:
            notebook = pickle.load(f)
            print("Notebook data deserialized.")
    except FileNotFoundError:
        notebook = Notebook()
        print("Notedata not found. Createda new one.")
    return address_book, notebook

def save_data(address_book, notebook):
    with open('address_book.pkl', 'wb') as f:
        pickle.dump(address_book, f)
        print("Address book data serialized.")

    with open('notebook.pkl', 'wb') as f:
        pickle.dump(notebook, f)
        print("Notebook data serialized.")

def main():
    global address_book, days
    address_book, notebook = load_data()

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command == 'hello':
            print("Hello! How can I help you?")
        elif command == 'add':
            name = args[0]
            phone = args[1]
            address = args[2]
            email = args[3] if len(args) > 3 else None
            birthday = args[4] if len(args) > 4 else None
            if len(args) > 5:
                birthday = args[5]
            result = address_book.add_contact(name, phone, address, email, birthday)
            print(result)
        elif command == 'delete':
            name = args[0]
            result = address_book.delete_contact(name)
            print(result)
        elif command == 'change':
            name = args[0]
            phone = args[1]
            result = address_book.change_phone(name, phone)
            print(result)
        elif command == 'phone':
            name = args[0]
            result = address_book.show_phones(name)
            print(result)
        elif command == 'birthday':
            name = args[0]
            if len(args) == 2:
                if name in address_book.contacts:
                    print(address_book.contacts[name].birthday)
                else:
                    print(f"Contact {name} not found.")
            elif len(args) == 3:
                birthday = args[2]
                if name in address_book.contacts:
                    address_book.contacts[name].birthday = birthday
                    print(f"Birthday for {name} added/changed to {birthday}.")
                else:
                    print(f"Contact {name} not found.")
            else:
                print("Invalid command. Usage: birthday <name> [birthday_date]")
        elif command == 'all':
            print(address_book.show_all_contacts())
        elif command == 'birthdays':
            days = args[0]
            result = address_book.birthdays(int(days))
            print(result)
        elif command == 'add_note':
            title = args[0]
            content = args[1]
            result = notebook.add_note(title, content)
            print(result)
        elif command == 'edit_note':
            title = args[0]
            new_content = args[1]
            result = notebook.edit_note(title, new_content)
            print(result)
        elif command == 'find_note':
            title = ' '.join(args)  # Join all arguments to form the title
            result = notebook.find_note(title)
            print(result)
        elif command == 'show_notes':
            all_notes = notebook.show_all_notes()
            print(all_notes)
        elif command == 'delete_note':
            title = args[0]
            result = notebook.delete_note(title)
            print(result)
        elif command == 'add_tag':
            title = args[0]
            tag = args[1]
            result = notebook.add_tag(title, tag)
            print(result)
        elif command == 'search_by_tag':
            tag = args[0]
            result = notebook.search_by_tag(tag)
            print(result)
        elif command in ["close", "exit"]:
            save_data(address_book, notebook)
            print("Goodbye!")
            break
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
