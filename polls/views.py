from typing import TypedDict

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Author, Book


class BookData(TypedDict):
    title: str
    pages: int
    author: str
    publisher: str | None
    is_long: bool


class BookDetailData(TypedDict):
    title: str
    pages: int
    author: str
    publisher: str | None
    description: str


class BookListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        books = Book.objects.select_related("author", "publisher").all()
        data: list[BookData] = [
            {
                "title": book.title,
                "pages": book.pages,
                "author": book.author.full_name,
                "publisher": book.publisher.title if book.publisher else None,
                "is_long": book.is_big_book(),
            }
            for book in books
        ]
        return JsonResponse(data, safe=False)


class BookDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        book = get_object_or_404(Book.objects.select_related("author", "publisher"), pk=pk)
        data: BookDetailData = {
            "pages": book.page_count,
            "author": book.author.full_name,
            "publisher": book.publisher.title if book.publisher else None,
            "description": book.long_description(),
        }
        return JsonResponse(data)


class AuthorBooksView(View):
    def get(self, request: HttpRequest, author_id: int) -> HttpResponse:
        author = Author.objects.filter(pk=author_id)
        books = author.books.all()
        data = {
            "author": author.full_name,
            "books": [book.name for book in books],
        }
        return JsonResponse(data)
