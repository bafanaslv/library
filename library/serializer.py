from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from library.models import Authors, Books, Lending
from library.validators import LibraryValidators


class AuthorsSerializer(ModelSerializer):

    class Meta:
        model = Authors
        fields = "__all__"


class BooksSerializer(ModelSerializer):

    # author = AuthorsSerializer(read_only=True)
    author = PrimaryKeyRelatedField(queryset=Authors.objects.all())

    class Meta:
        model = Books
        fields = "__all__"


class LendingSerializer(ModelSerializer):
    author = AuthorsSerializer()
    books = BooksSerializer()

    class Meta:
        model = Lending
        fields = "__all__"
        validators = [LibraryValidators()]
