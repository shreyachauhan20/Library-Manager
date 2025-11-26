import json
import logging
from typing import List, Optional
from pathlib import Path

from .book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, storage_path: str = "books.json"):
        self.storage = Path(storage_path)
        self.books: List[Book] = []
        # configure logging at module level if not already configured by application
        if not logging.getLogger().handlers:
            logging.basicConfig(level=logging.INFO,
                                format="%(asctime)s - %(levelname)s - %(message)s")
        logger.info("Initialized LibraryInventory with storage: %s", self.storage)
        self.load()

    def add_book(self, book: Book) -> None:
        if any(b.isbn == book.isbn for b in self.books):
            logger.error("Book with ISBN %s already exists.", book.isbn)
            raise ValueError(f"Book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        logger.info("Added book: %s", book)
        self.save()

    def search_by_title(self, title_query: str) -> List[Book]:
        q = title_query.strip().lower()
        results = [b for b in self.books if q in b.title.lower()]
        logger.info("Search by title '%s' found %d results.", title_query, len(results))
        return results

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                logger.info("Found book by ISBN %s: %s", isbn, b)
                return b
        logger.info("No book found with ISBN %s.", isbn)
        return None

    def display_all(self) -> List[str]:
        lines = [str(b) for b in self.books]
        logger.info("Displaying all books: %d total.", len(lines))
        return lines

    # Persistence
    def save(self) -> None:
        try:
            data = [b.to_dict() for b in self.books]
            with self.storage.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved %d books to %s", len(self.books), self.storage)
        except Exception as e:
            logger.exception("Failed to save books: %s", e)
            raise

    def load(self) -> None:
        if not self.storage.exists():
            logger.warning("Storage file %s does not exist. Starting with empty inventory.", self.storage)
            self.books = []
            return

        try:
            with self.storage.open("r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                # validate minimal shape
                if not all(k in item for k in ("title", "author", "isbn", "status")):
                    logger.error("Corrupted book record (missing keys): %s", item)
                    continue
                loaded.append(Book(**item))
            self.books = loaded
            logger.info("Loaded %d books from %s", len(self.books), self.storage)
        except json.JSONDecodeError as e:
            logger.exception("JSON decode error when loading %s: %s", self.storage, e)
            # Corrupt file: back it up and start empty
            try:
                backup = self.storage.with_suffix(self.storage.suffix + ".bak")
                self.storage.rename(backup)
                logger.error("Corrupted storage moved to %s. Starting with empty inventory.", backup)
            except Exception:
                logger.exception("Failed to back up corrupted storage file.")
            self.books = []
        except Exception as e:
            logger.exception("Unexpected error when loading storage: %s", e)
            self.books = []
