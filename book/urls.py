from django.urls import path
from .views import (
    BookListCreateAPIView, BookDetailAPIView,
    BorrowBookAPIView, ReturnBookAPIView, BorrowedBooksAPIView
)


urlpatterns = [
    path("list-create/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path("details/<int:book_id>/", BookDetailAPIView.as_view(), name="book-detail"),
    path('borrow/<int:book_id>/', BorrowBookAPIView.as_view(), name='borrow-book'),
    path('return/<int:book_id>/', ReturnBookAPIView.as_view(), name='return-book'),
    path('borrowed/', BorrowedBooksAPIView.as_view(), name='borrowed-books'),
]
