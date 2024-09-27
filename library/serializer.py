from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from library.models import Authors, Books


class AuthorsSerializer(ModelSerializer):

    class Meta:
        model = Authors
        fields = ["pk", "isni", "author"]


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"
