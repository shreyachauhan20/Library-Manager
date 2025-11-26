from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available" 


def __str__(self) -> str:
    return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"


def to_dict(self) -> Dict[str, str]:
    return asdict(self)


def is_available(self) -> bool:
    return self.status.lower() == "available"


def issue(self) -> bool:
    if self.is_available():
        self.status = "issued"
        return True
    return False


def return_book(self) -> bool:
    if not self.is_available():
        self.status = "available"
        return True
    return False
