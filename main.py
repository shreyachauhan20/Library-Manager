import sys
import logging

from library_manager.inventory import LibraryInventory
from library_manager.book import Book

logger = logging.getLogger(__name__)

MENU = '''
Library Manager
===============
1) Add Book
2) Issue Book
3) Return Book
4) View All Books
5) Search
6) Exit
Choose an option (1-6): '''


def safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Exiting.")
        sys.exit(0)


def add_book_cli(inv: LibraryInventory):
    title = safe_input("Title: ").strip()
    author = safe_input("Author: ").strip()
    isbn = safe_input("ISBN: ").strip()
    if not (title and author and isbn):
        print("All fields are required.")
        return
    try:
        book = Book(title=title, author=author, isbn=isbn)
        inv.add_book(book)
        print("Book added successfully.")
    except ValueError as e:
        print(e)


def issue_book_cli(inv: LibraryInventory):
    isbn = safe_input("ISBN to issue: ").strip()
    book = inv.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    if book.issue():
        inv.save()
        print("Book issued.")
    else:
        print("Book is already issued.")


def return_book_cli(inv: LibraryInventory):
    isbn = safe_input("ISBN to return: ").strip()
    book = inv.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    if book.return_book():
        inv.save()
        print("Book returned.")
    else:
        print("Book is already available.")


def view_all_cli(inv: LibraryInventory):
    lines = inv.display_all()
    if not lines:
        print("No books in inventory.")
        return
    for i, line in enumerate(lines, 1):
        print(f"{i}. {line}")


def search_cli(inv: LibraryInventory):
    sub = safe_input("Search by (t)itle or (i)sbn? ").strip().lower()
    if sub.startswith("t"):
        q = safe_input("Title query: ")
        results = inv.search_by_title(q)
        if not results:
            print("No matches.")
            return
        for b in results:
            print(b)
    elif sub.startswith("i"):
        isbn = safe_input("ISBN: ")
        book = inv.search_by_isbn(isbn)
        if book:
            print(book)
        else:
            print("Not found.")
    else:
        print("Unknown search type.")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    inv = LibraryInventory()
    while True:
        try:
            choice = safe_input(MENU).strip()
            if choice == "1":
                add_book_cli(inv)
            elif choice == "2":
                issue_book_cli(inv)
            elif choice == "3":
                return_book_cli(inv)
            elif choice == "4":
                view_all_cli(inv)
            elif choice == "5":
                search_cli(inv)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Enter a number between 1 and 6.")
        except Exception as e:
            logger.exception("An error occurred in main loop: %s", e)


if __name__ == "__main__":
    main()
