import data_handling
from notebook.notebook import Notebook
from notebook.address_book import AddressBook

def parse_input(user_input):
    command_parts = user_input.split(' ', 1)
    command = command_parts[0]
    args = command_parts[1].split(' ') if len(command_parts) > 1 else []
    return command, args

def main():
    global address_book, days
    address_book, notebook = data_handling.load_data()

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
            data_handling.save_data(address_book, notebook)
            print("Goodbye!")
            break
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()