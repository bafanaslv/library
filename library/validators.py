from rest_framework.serializers import ValidationError

from library.models import Books, Lending


class LibraryValidators:
    def __call__(self, value):
        lending_dict = dict(value)  # конвертируем QuerySet в словарь
        user_pk = lending_dict["user"].pk
        book_pk = lending_dict["book"].pk
        if lending_dict["operation"] == "issuance":
            # срабатывает при попытке повторно получить книгу с тем же названием если предыдущая не сдана.
            lending_objects_list = list(
                Lending.objects.filter(
                    user_id=user_pk, operation="issuance", book_id=book_pk, id_return=0
                )
            )
            if len(lending_objects_list) == 1:
                raise ValidationError("Вы уже получили эту книгу в библиотеке !")

        if (
            lending_dict["operation"] == "issuance"
            or lending_dict["operation"] == "write_off"
        ):
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
