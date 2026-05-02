import json

def print_menu():
        print("=== Contact Book ===")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Search contact")
        print("4. Delete contact")
        print("5. Quit")

def add_contact():
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        contacts = []

    print("Add contact:")
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")

    contacts_dict = {
         "name": name,
         "phone": phone,
         "email": email
    }

    contacts.append(contacts_dict)

    with open("contacts.json", "w") as f:
         json.dump(contacts, f)

def show_contacts():
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        contacts = []
    
    if not contacts:
        print("no contacts found!")
    else:
        for i, contact in enumerate(contacts):
            print(f"{i+1}. {contact['name']}, {contact['phone']} - {contact['email']}")

def search_user():
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        contacts = []

    search_string = input("Enter name to look for: ")
    found = False

    for c in contacts:
        if c['name'] == search_string:
            print(c['name'], c['phone'], c['email'])
            found = True

    if not found:
        print("User not found")

def delete_user():
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        contacts = []

    delete_string = input("Enter user to delete: ")
    
    found = False
    for c in contacts:
        if c['name'] == delete_string:
            contacts.remove(c)
            with open("contacts.json", "w") as f:
                json.dump(contacts, f)
            found = True
            break

    if not found:
        print("User not found")

user_input = ''

while user_input != '5':
    print_menu()
    user_input = input("Choose: ")
    if user_input == '1':
        add_contact()
    elif user_input == '2':
        show_contacts()
    elif user_input == '3':
        search_user()
    elif user_input == '4':
        delete_user()
    elif user_input == '5':
        print('Quitting...')
    else:
        print("not a valid option! - try again")