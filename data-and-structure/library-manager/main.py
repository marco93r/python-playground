class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def borrow(self):
        self.is_available = False

    def return_book(self):
        self.is_available = True

    def __repr__(self):
        return self.title

def print_menu():
        print("=== Library Manager ===")
        print("1. Add book")
        print("2. Borrow book")
        print("3. Return book")
        print("4. Show all books")
        print("5. Quit")

def main():
    books = []
    user_input = ''

    while user_input != '5':
         
        print_menu()
        user_input = input("Choose: ")

        if user_input == '1':
            title = input('Enter book title: ')
            author = input('Enter author of the book: ')
            is_available = True
            b = Book(title, author)
            books.append(b)

        elif user_input == '2':
            print(books)
            b = input('Enter book you want to borrow: ')
            for book in books:
                if book.title == b and book.is_available:
                    book.borrow()
                    break
                else:
                    print('Book not found or is already borrowed!')

        elif user_input == '3':
            b = input('Enter book you want to return: ')
            for book in books:
                if book.title == b and book.is_available == False:
                    book.return_book()
                    break
                else:
                    print('You cant return this book')

        elif user_input == '4':
            available_books = []
            unavailable_books = []
            for book in books:
                if book.is_available == True:
                    available_books.append(book)
                else:
                    unavailable_books.append(book)

            print('Available Books: ')
            for book in available_books:
                print(book)

            print('Unavailable Books:')
            for book in unavailable_books:
                print(book)

        elif user_input == '5':
            print('Quitting ...')

        else:
            print('Not a valid option, try again!')

main()

