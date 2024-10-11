from rest_framework.serializers import ValidationError
from library.models import Lending, Books


class LibraryValidators:
    def __call__(self, value):
        lending_dict = dict(value)  # конвертируем QuerySet в словарь

        if lending_dict["operation"] == "issuance":
            # срабатывает при попытке повторно получить книгу с тем же названием если предыдущая не сдана.
            lending_objects_list = list(Lending.objects.filter(book_id=lending_dict["book"].pk, id_return=0))
            for lending_objects in lending_objects_list:
                if lending_objects.date_event is None:
                    raise ValidationError(
                        "Вы уже получили эту книгу в библиотеке !"
                    )

        if lending_dict["operation"] == "issuance" or lending_dict["operation"] == "write_off":
            book_object = Books.objects.get(pk=lending_dict["book"].pk)
            if book_object.quantity_all == 0:
                # срабатывает при попытке выдать или списать книги, которые еще не поступили в библиотеку.
                raise ValidationError(
                        f"Книги '{book_object.name}' еще не поступили в библиотеку !"
                    )
            elif book_object.quantity_all == book_object.quantity_lending:
                # срабатывает при попытке выдать книгу, которых нет в библиотеке (на руках у читателей)
                raise ValidationError(
                        f"Все книги '{book_object.name}' выданы читателям !"
                    )
