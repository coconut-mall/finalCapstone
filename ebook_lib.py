# ==== Imports ==== #
# Tabulate used for printing tables and records in a clean format
from tabulate import tabulate


# ==== Class ==== #
class Book:

    # Define class properties matching fields in the database table
    def __init__(self, id, title, author, qty) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.qty = qty

    # Returns the object's properties as a tuple
    # Used for inserting as a record into the db
    def get_tuple(self):
        return (self.id, self.title, self.author, self.qty)

    # Adds the object as a record into the database table
    def add(self, cursor):
        """Pass cursor as argument"""

        # Try to run SQL to add obj to the table
        try:
            cursor.execute(
                """
        INSERT INTO books
        VALUES
            (?, ?, ?, ?)""",
                self.get_tuple(),
            )
            print_query([self.get_tuple()])
            print("Book added successfully")

        # If there is an error then the record already exists
        except:
            print("Book already exists")


# ==== Variables ==== #
# Defined headers used with tabulate module
HEADERS = ["id", "Title", "Author", "Qty"]


# ==== Functions ==== #
# Creates a unique id number for a book object
def create_id(cursor):
    """Pass cursor as argument"""

    # Try to get the highest id no. from all records in the table
    try:
        cursor.execute("SELECT MAX(id) FROM books")

        # Add 1 to the highest id to get the new id and return it
        new_id = cursor.fetchone()[0] + 1
        return new_id

    # If there is an error then the table is empty so new id is 3001
    except:
        return 3001


# Loops until user enters a valid integer then returns it
def get_qty():

    while True:
        print("Add a quantity for the book:")
        value = input()

        try:
            value = int(value)
            return value

        except:
            continue


# Gets info and creates a new book object
def create_book(new_id):
    """Pass new id as argument"""

    # Get the information for the new book
    new_title = input("Enter a title for the book:\n")
    new_author = input("Enter the authors name:\n")
    new_qty = get_qty()

    # Create a new book object using the info and return it
    return Book(new_id, new_title, new_author, new_qty)


# Selects every record from the table and returns the selection
def get_all(cursor):
    """Pass cursor as the argument"""
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()


# Uses tabulate to print the results of a query in a readable format
def print_query(query):

    # If the query is empty then no results were found
    if len(query) == 0:

        # Print error message and return
        print("Record not found")
        return

    # Else results were found so print them in a table and return 1
    else:
        print(tabulate(query, headers=HEADERS, tablefmt="github"))
        return 1


# User can decide how they want to search for a book
def search_select():
    valid_inputs = ["1", "2", "3", "0"]

    # Loop for valid input
    while True:
        print("How do you want to search?")
        print(
            """
1  id
2  Title
3  Author
0  main menu"""
        )
        choice = input()

        # If input is valid then return it
        if choice in valid_inputs:
            return choice

        # Else loop
        print("Invalid input")


# Allows user to select a book by id
def search_id(cursor):
    """Pass cursor as the argument"""

    # User enters the id
    print("Enter the book's id")
    search_id = input()

    # Select all records that match that id
    cursor.execute("SELECT * FROM books WHERE id = (?)", (search_id,))

    # Save selection to a variable
    query = cursor.fetchall()

    # Return the id used to search and the table selection
    return search_id, query


# Allows user to search for a book by its title
def search_title(cursor):
    """Pass cursor as argument"""
    # User enters title
    print("Enter book's title")
    search_title = input()

    # Select records which match that tile
    cursor.execute("SELECT * FROM books WHERE title = (?)", (search_title,))

    # Print the selection
    print_query(cursor.fetchall())


# Allows user to search for a book by its author
def search_author(cursor):
    """Pass cursor as argument"""
    # User enters author
    print("Enter the book's author")
    search_author = input()

    # Select records which match that author
    cursor.execute("SELECT * FROM books WHERE author = (?)", (search_author,))

    # Print the selection
    print_query(cursor.fetchall())


# Allows user to update the qty for a book
def update_book(cursor, search_id):
    """Takes in the cursor and the id for the book to be updated as arguments"""

    # Get new qty from the user
    new_qty = get_qty()

    # Update book with the given id with the new qty
    cursor.execute(
        """
    UPDATE books
    SET Qty = (?)
    WHERE id = (?)
    """,
        (new_qty, search_id),
    )

    # Select the record that matches the given id
    cursor.execute("SELECT * FROM books WHERE id = (?)", (search_id,))

    # Print the updated record
    print()
    print_query(cursor.fetchall())


# Allows user to delete a book record
def delete_book(cursor, search_id):
    """Pass cursor and a book id as arguments"""

    # Loop for user input
    while True:

        # Double check user wants to delete this record
        print("Are you sure you want to delete this record? (y/n)")
        choice = input()

        # If yes delete the record and print confirmation
        if choice == "y":
            cursor.execute("DELETE FROM books WHERE id = (?)", (search_id,))
            print("Record deleted")
            return

        # If no then exit function
        elif choice == "n":
            return

        # Else input is invalid
        else:
            print("Invalid Input")
