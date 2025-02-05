from django.urls import path
from .views import BookListCreateAPIView, BookDetailAPIView


urlpatterns = [
    path("list-create/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path("details/<int:book_id>/", BookDetailAPIView.as_view(), name="book-detail"),
]
