from rest_framework.serializers import ModelSerializer
from library.models import Authors, Books, Lending
from library.validators import LibraryValidators
from users.serializer import UserSerializerReadOnly


class AuthorsSerializerReadOnly(ModelSerializer):

    class Meta:
        model = Authors
        fields = ("author",)


class AuthorsSerializer(ModelSerializer):

    class Meta:
        model = Authors
        fields = ("author",)


class BooksSerializerReadOnly(ModelSerializer):
    author = AuthorsSerializerReadOnly(read_only=True)

    class Meta:
        model = Books
        fields = ("author", "name",)


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"


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
