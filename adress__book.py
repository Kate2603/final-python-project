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
