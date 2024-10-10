from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from library.models import Authors, Books, Lending
from library.paginations import AuthorsPaginator, BooksPaginator, LendingPaginator
from library.serializer import AuthorsSerializer, BooksSerializer, BooksSerializerReadOnly, LendingSerializer, \
    LendingSerializerReadOnly
from users.permissions import IsLibrarian


class AuthorsViewSet(viewsets.ModelViewSet):

    queryset = Authors.objects.all().order_by('id')
    serializer_class = AuthorsSerializer
    pagination_class = AuthorsPaginator

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ("author",)
    search_fields = ("author",)

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            self.permission_classes = (IsLibrarian,)
        return super().get_permissions()


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all().order_by('id')
    pagination_class = BooksPaginator

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return BooksSerializer
        else:
            return BooksSerializerReadOnly

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ("author", "genre", "name",)
    search_fields = ("author", "name",)
    filterset_fields = ("author", "genre", "name", "barcode")

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            self.permission_classes = (IsLibrarian,)
        return super().get_permissions()


class LendingListApiView(ListAPIView):
    def get_queryset(self):
        if IsLibrarian().has_permission(self.request, self):
            return Lending.objects.all().order_by('id')
        else:
            return Lending.objects.filter(user=self.request.user)

    serializer_class = LendingSerializerReadOnly
    pagination_class = LendingPaginator

    filter_backends = [OrderingFilter, DjangoFilterBackend,]
    ordering_fields = ("book",)
    filterset_fields = ("user", "book", "date_event",)


class LendingCreateApiView(CreateAPIView):
    """Создавать могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_create(self, serializer):
        operation = serializer.validated_data["operation"]
        book_id = serializer.validated_data["book"].pk
        book_name = serializer.validated_data["book"].name
        quantity = serializer.validated_data["arrival_quantity"]
        book_object = Books.objects.get(pk=book_id)
        lending = serializer.save()
        if operation == "arrival":
            if serializer.validated_data["user"].pk != self.request.user.id:
                raise ValidationError(
                    f"У читателя '{serializer.validated_data["user"].reader_name}' отсуствуют права на регистрацию поступления книг !"
                )
            book_object.quantity_all += quantity
        elif operation == "issuance":
            book_object.quantity_lending += 1
            book_object.amount_lending += 1
        elif operation == "return":
            book_object.quantity_lending -= 1
        elif operation == "write_off":
            book_object.quantity_all -= 1
        elif operation == "loss":
            print(f"Книга {book_name} утеряна, необходимо провести списание книги.")

        book_object.save()
        lending.save()
    permission_classes = [IsLibrarian]


class LendingRetrieveApiView(RetrieveAPIView):
    """Просматривать отдельного могут авторизованный пользователь, который является владельцем или модератором."""

    def get_queryset(self):
        if IsLibrarian().has_permission(self.request, self):
            return Lending.objects.all()
        else:
            return Lending.objects.filter(user=self.request.user)

    queryset = Lending.objects.all()
    serializer_class = LendingSerializerReadOnly


class LendingUpdateApiView(UpdateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_update(self, serializer):
        lending_object = Lending.objects.get(pk=self.kwargs['pk'])
        if lending_object.date_event is not None:
            raise ValidationError(
                        "Книга возвращена читателем - повторный возврат невозможен !"
                    )
        book_json_id = serializer.validated_data["book"].pk
        book_object = Books.objects.get(pk=book_json_id)
        book_object.quantity_lending -= 1
        book_object.amount_lending -= 1
        book_object.save()
        lending = serializer.save()
        lending.save()

    permission_classes = [IsLibrarian]


class LendingDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""

    def get_queryset(self):
        lending_object = Lending.objects.get(pk=self.kwargs['pk'])
        if lending_object.date_event is not None:
            raise ValidationError(
                        "Книга возвращена читателем - удаление выдачи невозможно !"
                    )
        book_object = Books.objects.get(pk=lending_object.book_id)
        book_object.quantity_lending -= 1
        book_object.save()
        return Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = [IsLibrarian]
