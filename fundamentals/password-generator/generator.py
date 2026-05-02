import random, string, json

def print_menu():
    print("=== Password Generator ===")
    print("1. Generate password")
    print("2. Save password")
    print("3. Show saved password")
    print("4. Quit")

def generate_password():
    while True:
        length = input('Choose password length: ')
        if length.isdigit():
            break
        print('Invalid input')

    while True:
        if int(length) > 8:
            break
        print('Too short, try again!')
        length = input('Choose password length: ')

    while True:
        uppercase = input('Uppercase letters? (y/n): ')
        if uppercase == 'y' or uppercase == 'n':
            break
        print('Invalid input')
        
    while True:
        lowercase = input('Lowercase letters? (y/n): ')
        if lowercase == 'y' or lowercase == 'n':
            break
        print('Invalid input')
    
    while True:
        numbers = input('Numbers? (y/n): ')
        if numbers == 'y' or numbers == 'n':
            break
        print('Invalid input')
        
    while True:
        special_chars = input('Special characters? (y/n): ')
        if special_chars == 'y' or special_chars == 'n':
            break
        print('Invalid input')

    chars = ''
    
    if lowercase == 'y':
        chars += string.ascii_lowercase
    if uppercase == 'y':
        chars += string.ascii_uppercase
    if numbers == 'y':
        chars += string.digits
    if special_chars == 'y':
        chars += string.punctuation

    password = ''.join(random.choice(chars) for _ in range(int(length)))

    print("Generated password: ", password)
    return password
    

def save_password(password):
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        passwords = []

    description = input('Description for the password: ')
    value = password

    password_dict = {
        "description": description,
        "value": value
    }

    passwords.append(password_dict)

    with open("passwords.json", "w") as f:
        json.dump(passwords, f)

def show_passwords():
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        passwords = []
    
    if not passwords:
        print("no passwords found!")
    else:
        for i, password in enumerate(passwords):
            print(f"{i+1}. {password['description']}: {password['value']}")

user_input = ''
password = None

while user_input != '4':
    print_menu()
    user_input = input("Choose: ")
    if user_input == '1':
        password = generate_password()
    elif user_input == '2':
        if password is None:
            print('Generate a password first!')
        else:
            save_password(password)
    elif user_input == '3':
        show_passwords()
    elif user_input == '4':
        print('Quitting...')
    else:
        print("not a valid option! - try again")