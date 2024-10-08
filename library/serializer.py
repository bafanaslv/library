from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from library.models import Authors, Books, Lending
from library.validators import LibraryValidators
from users.models import Users
from users.serializer import UserSerializerReadOnly


class AuthorsSerializerReadOnly(ModelSerializer):

    class Meta:
        model = Authors
        fields = ("id", "author",)


class AuthorsSerializer(ModelSerializer):

    class Meta:
        model = Authors
        fields = "__all__"


class BooksSerializerReadOnly(serializers.ModelSerializer):
    author = AuthorsSerializerReadOnly(read_only=True)

    class Meta:
        model = Books
        fields = ("id", "author", "name",)


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = ("author", "name", "genre",)


class LendingSerializerReadOnly(ModelSerializer):
    user = UserSerializerReadOnly(read_only=True)

    class Meta:
        model = Lending
        fields = "__all__"


class LendingSerializer(ModelSerializer):

    class Meta:
        model = Lending
        fields = ("user", "book", "operation", "date_event", "arrival_quantity",)
        validators = [LibraryValidators()]
