from rest_framework.serializers import ValidationError

from library.models import Books


class LibraryValidators:
    def __call__(self, value):
        val = dict(value)  # конвертируем QuerySet в словарь
        id_book = val["book"].pk
        book_object = Books.objects.get(pk=id_book)
        print(book_object.pk)
        if book_object:
            raise ValidationError(
                "вы уже получали эту книгу в библиотетке !"
            )
