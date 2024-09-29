from rest_framework.serializers import ValidationError

from library.models import Lending


class LibraryValidators:
    def __call__(self, value):
        val = dict(value)  # конвертируем QuerySet в словарь
        book_id = val["book"].pk
        book_object = Lending.objects.get(id_book=book_id)
        print(book_object.pk)
        if book_object:
            raise ValidationError(
                "вы уже получали эту книгу в библиотетке !"
            )
