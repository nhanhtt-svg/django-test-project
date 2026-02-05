import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from polls.models import Author, Book, Publisher


@pytest.mark.django_db
def test_book_str():
    author = Author.objects.create(name="Nhan", age=30)
    book = Book.objects.create(title="Test Book", pages=123, author=author)
    assert str(book) == "Test Book"


@pytest.mark.django_db
def test_book_is_long_book():
    author = Author.objects.create(name="Nhan", age=30)
    book = Book.objects.create(title="Long Book", pages=600, author=author)
    assert book.is_long_book() is True


@pytest.mark.django_db
def test_book_short_description():
    author = Author.objects.create(name="Nhan", age=30)
    book = Book.objects.create(title="Short Book", pages=100, author=author)
    assert "Short Book" in book.short_description()


@pytest.mark.django_db
def test_book_list_view(client: Client):
    author = Author.objects.create(name="Nhan", age=30)
    publisher = Publisher.objects.create(name="NXB", country="VN")
    Book.objects.create(title="Book1", pages=200, author=author, publisher=publisher)

    url = reverse("book-list") 
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Book1"
    assert data[0]["author"] == "Nhan"


@pytest.mark.django_db
def test_book_detail_view(client: Client):
    author = Author.objects.create(name="Nhan", age=30)
    book = Book.objects.create(title="Book2", pages=300, author=author)

    url = reverse("book-detail", args=[book.pk])
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book2"
    assert data["author"] == "Nhan"


@pytest.mark.django_db
def test_author_books_view(client: Client):
    author = Author.objects.create(name="Nhan", age=30)
    Book.objects.create(title="Book3", pages=150, author=author)

    url = reverse("author-books", args=[author.pk])
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["author"] == "Nhan"
    assert "Book3" in data["books"]
