from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from book.models import Book
from user_manages.permission import IsAdminUser
from book.serializers import BookSerializer



class APITesting(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        book_data = Book.objects.all()
        serialize = BookSerializer(book_data, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        book_serializer = BookSerializer(request.data)
        if book_serializer.is_valid():
            book_serializer.save()
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
