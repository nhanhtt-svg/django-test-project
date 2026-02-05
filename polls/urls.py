from django.urls import path

from .views import AuthorBooksView, BookDetailView, BookListView

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("authors/<int:author_id>/books/", AuthorBooksView.as_view(), name="author-books"),
]
