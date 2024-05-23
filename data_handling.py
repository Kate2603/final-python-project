import pickle
from notebook.notebook import Notebook
from notebook.address_book import AddressBook

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
        print("Notebook data not found. Created a new one.")
    return address_book, notebook

def save_data(address_book, notebook):
    with open('address_book.pkl', 'wb') as f:
        pickle.dump(address_book, f)
        print("Address book data serialized.")

    with open('notebook.pkl', 'wb') as f:
        pickle.dump(notebook, f)
        print("Notebook data serialized.")