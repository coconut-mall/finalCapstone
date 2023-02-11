# ====Startup====#

# Imports
import sqlite3

# Import custom module with functions and book class
import ebook_lib
from ebook_lib import Book


# Connect/start database, create cursor object
db = sqlite3.connect("ebookstore")
c = db.cursor()


# Create table if one doesn't already exist
c.execute(
    """
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY,
    Title VARCHAR UNIQUE, 
    Author VARCHAR, 
    Qty int
    );"""
)


# Def list of starting records
dummy_records = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.k. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C.S.Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
]


# Turn records into book objects and add to books table
for record in dummy_records:
    new_book = Book(*record)
    new_book.add(c)

print()

# Print the table as it stands at the start of the program
ebook_lib.print_query(ebook_lib.get_all(c))




# Main menu loop
while True:

    # Print menu options to the user
    print()
    print("Select an option from the menu below")
    print(
        """
1  Enter Book
2  Update Book
3  Delete Book
4  Search Book
0  Exit
    """
    )

    # Get user input
    choice = input()
    print()

    # Add a new book record to the database
    if choice == "1":

        # Create a unique id for the record
        new_id = ebook_lib.create_id(c)

        # Create a new book object
        new_book = ebook_lib.create_book(new_id)
        print()

        # Call the objects .add method to add it to the database
        new_book.add(c)
        print()

    # Update the qty for a book record
    elif choice == "2":

        # Get the id from user and select record matching that id from the table
        book_id, query = ebook_lib.search_id(c)
        print()

        # Try to print the matching record
        record_found = ebook_lib.print_query(query)

        # If a record is found then the print_function will have returned 1
        if record_found == 1:

            # Run update book function which will get a qty from the user and update the record
            print()
            ebook_lib.update_book(c, book_id)

    # Delete a record from the database
    elif choice == "3":

        # Get id from the user and select record matching that id from the table
        book_id, query = ebook_lib.search_id(c)

        # Try to print the matching record
        record_found = ebook_lib.print_query(query)

        # If a record was found then the print_function will have returned 1
        if record_found == 1:

            # Delete the record that matches the given id
            ebook_lib.delete_book(c, book_id)

    # Search for a book record
    elif choice == "4":

        # User chooses how they want to search for the book
        choice = ebook_lib.search_select()

        # Search by id
        if choice == "1":

            # Get id from user and select records matching that id
            search_id, query = ebook_lib.search_id(c)

            # Try to print the records
            ebook_lib.print_query(query)

        # Search by title
        elif choice == "2":

            # Get a title from the user and try to print records that match that title
            ebook_lib.search_title(c)

        # Search by author
        elif choice == "3":

            # Get and author from the user and try to print records matching that author
            ebook_lib.search_author(c)

    # Exit function and commit changes to the database
    elif choice == "0":
        db.commit()
        exit()

    # Input is invalid so loop
    else:
        print("Invalid selection")
