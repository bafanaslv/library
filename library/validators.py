from rest_framework.serializers import ValidationError

from library.models import Lending


class LibraryValidators:
    def __call__(self, value):
        val = dict(value)  # конвертируем QuerySet в словарь
        book_object = list(Lending.objects.filter(book_id=val["book"].pk))
        for book in book_object:
            if book.date_return is None:
                raise ValidationError(
                    "вы уже получали эту книгу в библиотеке !"
                )
