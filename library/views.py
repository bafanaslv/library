# Проект предназначен для созалания REST API для управления библиотекой и предназначен для выполнения всех функции
# по отслеживанию движения книг от поступления в библиотеку до момента их списани по причинам физического износа или
# утери читателем.

# В проекте созданы три модели: авторы книг (Authors), собственно книги (Books) и операции по библитеке (Lendings).
# Операции по библиотеке - поступление, выдача читетелю, возврат в библиотеку, списание книги и утеря книги.
# Все операции можно отменять, если они не нарушают целостность базы данных.
# Предусмотрены различные варианты фильтрации и поиска в операциях, позволяющие находить нужную информацию как читателю
# так и бибиотекарю. Опираясь на данную информацию библитекарь в то числе может строить разнообразные отчеты
# (вышестоящие органы, в статистику и так далее)


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from library.models import Authors, Books, Lending
from library.paginations import (AuthorsPaginator, BooksPaginator,
                                 LendingPaginator)
from library.serializer import (AuthorsSerializer, BooksSerializer,
                                BooksSerializerReadOnly, LendingSerializer,
                                LendingSerializerReadOnly,
                                LendingSerializerWriteOff)
from users.permissions import IsLibrarian


class AuthorsViewSet(viewsets.ModelViewSet):
    """Представление для авторов книг"""

    queryset = Authors.objects.all().order_by("id")
    serializer_class = AuthorsSerializer
    pagination_class = AuthorsPaginator

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ("author",)
    search_fields = ("author",)

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            self.permission_classes = (
                IsLibrarian,
                IsAuthenticated,
            )
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class BooksViewSet(viewsets.ModelViewSet):
    """Представление для книг."""

    queryset = Books.objects.all().order_by("id")
    pagination_class = BooksPaginator

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return BooksSerializer
        else:
            return BooksSerializerReadOnly

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = (
        "author",
        "genre",
        "name",
    )
    search_fields = (
        "author",
        "name",
    )
    filterset_fields = ("author", "genre", "name", "barcode")

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            self.permission_classes = (
                IsLibrarian,
                IsAuthenticated,
            )
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class LendingListApiView(ListAPIView):
    def get_queryset(self):
        if IsLibrarian().has_permission(self.request, self):
            return Lending.objects.all().order_by("id")
        else:
            return Lending.objects.filter(user=self.request.user)

    serializer_class = LendingSerializerReadOnly
    pagination_class = LendingPaginator

    filter_backends = [
        OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ("book", "user", "date_event")
    filterset_fields = (
        "user",
        "book",
        "date_event",
        "operation",
        "is_return",
        "is_loss",
        "is_write_off",
    )


class LendingCreateApiView(CreateAPIView):
    """Создавать операции в библиотеке могут только пользователи с правами библиоткаря.
    Результаты каждой операции по библиотеке, помимо модели Lendings, отражажаются в модели Books.
    """

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_create(self, serializer):
        operation = serializer.validated_data["operation"]
        book_return_id = serializer.validated_data["book"].pk
        book_user_id = serializer.validated_data["user"].pk
        book_name = serializer.validated_data["book"].name
        book_object = Books.objects.get(pk=book_return_id)
        if operation == "inventory":
            # при поступлении партии книг увеличивается общее количество книг с таким названием (quantity_all)
            # пользователем (хозяином) операции в этом случае автоматически является библиотекарь
            serializer.validated_data["user"].pk = self.request.user.id
            quantity = serializer.validated_data["arrival_quantity"]
            issued = serializer.validated_data["issued_quantity"]
            book_object.quantity_all += quantity
            book_object.quantity_lending += issued
        if operation == "arrival":
            # при поступлении партии книг увеличивается общее количество книг с таким названием (quantity_all)
            # пользователем (хозяином) операции в этом случае автоматически является библиотекарь
            serializer.validated_data["user"].pk = self.request.user.id
            quantity = serializer.validated_data["arrival_quantity"]
            book_object.quantity_all += quantity
        elif operation == "issuance":
            # при получениии книг увеличивается количество выданных с данным названием книг (quantity_lending)
            # и общее количество выдачи (amount_lending)
            book_object.quantity_lending += 1
            book_object.amount_lending += 1
        elif operation == "return":
            # при возврате книги уменьшается количество выданных с данным названием книг (quantity_lending)
            # далее в БД ищется операция выдачи книги пользователю и делается пометка о возврате (is_return = True)
            # при попытке повторного возврата появляется исключение
            lending_object_list = list(
                Lending.objects.filter(
                    user_id=book_user_id,
                    operation="issuance",
                    book_id=book_return_id,
                    id_return=0,
                )
            )  # поиск операции выдачи книги
            if len(lending_object_list) == 0:
                raise ValidationError(f"Книга '{book_object.name}' уже возвращена !")
            lending_object_id = lending_object_list[0].pk  # id операции выдачи книги
            lending_object = Lending.objects.get(
                pk=lending_object_id
            )  # найденная операция выдачи
            book_object.quantity_lending -= 1
        elif operation == "write_off":
            # при списании физически изношенной книги уменьшается общее количество данных книг (quantity_all)
            # пользователем (хозяином) операции в этом случае автоматически является библиотекарь
            serializer.validated_data["user"].pk = self.request.user.id
            book_object.quantity_all -= 1
        elif operation == "loss":
            # при утере книги отправляется сообщение библиотекарю о необходимости списания книги
            # пользователем (хозяином) операции в этом случае автоматически является библиотекарь
            # БД ищется операция выдачи книги пользователю и делается пометка о возврате
            # Общее количество книги в библиотеке уменьшатеся на 1
            serializer.validated_data["user"].pk = self.request.user.id
            print(f"Книга {book_name} утеряна, необходимо провести списание книги.")
            lending_object_list = list(
                Lending.objects.filter(
                    user_id=book_user_id,
                    operation="issuance",
                    book_id=book_return_id,
                    id_return=0,
                )
            )  # поиск операции выдачи книги
            if len(lending_object_list) == 0:
                raise ValidationError(f"Книга '{book_object.name}' возвращена !")
            lending_object_id = lending_object_list[0].pk  # id операции выдачи книги
            lending_object = Lending.objects.get(
                pk=lending_object_id
            )  # найденная операция выдачи
            book_object.quantity_all -= 1
            book_object.amount_lending -= 1

        lending = serializer.save()
        book_object.save()
        lending.save()
        if operation == "return":
            # пометка о возврате книги в операции выдачи книги
            lending_object.id_return = lending.id
            lending_object.is_return = True
            lending_object.save()

        if operation == "loss":
            # пометка об утере книги в операции выдачи книги
            lending_object.id_return = lending.id
            lending_object.is_loss = True
            lending_object.save()

    permission_classes = [IsLibrarian]


class LendingDestroyApiView(DestroyAPIView):
    """Удалять операции по библиотеке могут только пользователи с правами библиотекаря."""

    def get_queryset(self):
        lending_object = Lending.objects.get(pk=self.kwargs["pk"])  # удаляемая операция
        book_object = Books.objects.get(
            pk=lending_object.book_id
        )  # книга связанная с удаляемой операцией
        if lending_object.operation == "arrival":
            # удаление партии поступивших книг
            if (
                book_object.quantity_all - book_object.quantity_lending
                < lending_object.arrival_quantity
            ):
                raise ValidationError(
                    f"Количество выданных книг '{book_object.name}' превысит их общее количество в библиотеке!"
                    f" Удаление поступления невозможно !"
                )
            book_object.quantity_all -= lending_object.arrival_quantity
        elif lending_object.operation == "issuance":
            # удаление выдачи книги удаление невозможно если операция помечена возвратом (id_return > 0).
            if lending_object.id_return > 0:
                if lending_object.is_return > 0:
                    raise ValidationError(
                        f"Невоможно удалить выдачу книги '{book_object.name}' - она возвращена или утеряна!"
                    )
                else:
                    raise ValidationError(
                        f"Невоможно удалить выдачу книги '{book_object.name}' - она утеряна!"
                    )

            # при возврате книг уменьшается количество выданных книг читателям (quantity_lending)
            # и общее количество выдачи (amount_lending)
            book_object.quantity_lending -= 1
            book_object.amount_lending -= 1
        elif lending_object.operation == "write_off":
            # при удалении списании книг увеличивается общее количество книг с данным названием (quantity_all)
            book_object.quantity_all += 1
        if lending_object.operation == "return":
            # при удалении возврата книги увеличивается общее количество выданных книг с данным названием (quantity_all)
            # далее в БД ищется операция выдачи книги и улаляется пометка о возврате (id_return = 0, is_return = False)
            lending_issuance_object = Lending.objects.get(id_return=lending_object.pk)
            lending_issuance_object.id_return = 0
            lending_issuance_object.is_return = False
            lending_issuance_object.save()
            book_object.quantity_lending += 1
        if lending_object.operation == "loss":
            # в БД ищется операция выдачи книги и удаляется пометка об утере (id_return = 0, is_loss = False)
            # невозможно выполнить эту операцию если книга после утери списана.
            # при удалении операции потери общее количество книги в библиотеке увеличивается на 1 (quantity_all += 1)
            lending_issuance_object = Lending.objects.get(id_return=lending_object.pk)
            if lending_issuance_object.is_write_off:
                raise ValidationError(
                    f"Невоможно удалить утерю - книга '{book_object.name}' списана !"
                )
            lending_issuance_object.id_return = 0
            lending_issuance_object.is_loss = False
            lending_issuance_object.save()
            book_object.quantity_all += 1
        book_object.save()
        return Lending.objects.all()

    permission_classes = [IsLibrarian]
    serializer_class = LendingSerializer


class LendingRetrieveApiView(RetrieveAPIView):
    """Просматривать отдельную операцию могут только авторизованные пользователи или библиотекарь."""

    def get_queryset(self):
        if IsLibrarian().has_permission(self.request, self):
            return Lending.objects.all()
        else:
            return Lending.objects.filter(user=self.request.user)

    queryset = Lending.objects.all()
    serializer_class = LendingSerializerReadOnly


class LendingUpdateApiView(UpdateAPIView):
    """Изменения проводятся только для списания и отмены списания утерянной книги."""

    queryset = Lending.objects.all()
    serializer_class = LendingSerializerWriteOff

    def perform_update(self, serializer):
        """Перед сохраннием операции проверяем действительно ли она утеряна."""
        lending_object = Lending.objects.get(
            pk=self.kwargs["pk"]
        )  # изменяемая операция

        if lending_object.operation == "issuance" and lending_object.is_loss:
            lending = serializer.save()
            lending.save()
        else:
            raise ValidationError(f"Можно списать только утерянную книгу.")

    permission_classes = [IsLibrarian]
