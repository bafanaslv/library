from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from library.models import Authors, Books, Lending
from library.validators import LibraryValidators
from users.serializer import UserSerializerReadOnly


class AuthorsSerializerReadOnly(ModelSerializer):

    class Meta:
        model = Authors
        fields = (
            "author",
        )


class AuthorsSerializer(ModelSerializer):

    class Meta:
        model = Authors
        fields = "__all__"


class BooksSerializerReadOnly(serializers.ModelSerializer):
    author = AuthorsSerializerReadOnly(read_only=True)

    class Meta:
        model = Books
        fields = (
            "id",
            "author",
            "name",
            "genre",
            "quantity_all",
            "quantity_lending",
            "amount_lending",
        )


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = (
            "author",
            "name",
            "genre",
        )


class LendingSerializerReadOnly(ModelSerializer):
    user = UserSerializerReadOnly(read_only=True)

    class Meta:
        model = Lending
        fields = "__all__"


class LendingSerializer(ModelSerializer):

    class Meta:
        model = Lending
        fields = "__all__"
        validators = [LibraryValidators()]


class LendingSerializerWriteOff(ModelSerializer):
    """Данный сериализатор предназначен для списания утерянной книги."""

    class Meta:
        model = Lending
        fields = ("is_write_off",)
