from rest_framework.serializers import ValidationError

from library.models import Lending, Books


class LibraryValidators:
    def __call__(self, value):
        lending_dict = dict(value)  # конвертируем QuerySet в словарь
        if lending_dict["date_return"] is None:
            lending_objects_list = list(Lending.objects.filter(book_id=lending_dict["book"].pk, date_return=None))
            print(lending_objects_list)
            for lending_objects in lending_objects_list:
                if lending_objects.date_return is None:
                    raise ValidationError(
                        "Вы уже получили эту книгу в библиотеке !"
                    )

            book_object = Books.objects.get(pk=lending_dict["book"].pk)
            if book_object.quantity_all == book_object.quantity_lending:
                raise ValidationError(
                        f"Все книги '{book_object.name}' выданы читателям !"
                    )
