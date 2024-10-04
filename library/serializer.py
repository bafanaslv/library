from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from library.models import Authors, Books, Lending
from library.validators import LibraryValidators


class AuthorsSerializer(ModelSerializer):

    class Meta:
        model = Authors
        fields = "__all__"


class BooksSerializerReadOnly(ModelSerializer):
    author = AuthorsSerializer(read_only=True)

    class Meta:
        model = Books
        fields = "__all__"


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"


class LendingSerializerReadOnly(ModelSerializer):
    author = AuthorsSerializer(read_only=True)
    books = BooksSerializer(read_only=True)

    class Meta:
        model = Lending
        fields = "__all__"


class LendingSerializer(ModelSerializer):
    class Meta:
        model = Lending
        fields = "__all__"
        validators = [LibraryValidators()]
