from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from library.models import Authors, Books, Lending
from library.serializer import AuthorsSerializer, BooksSerializer, LendingSerializer
from users.permissions import IsLibrarian


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            self.permission_classes = (IsLibrarian,)
        return super().get_permissions()


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("author", "genre")
    filterset_fields = ("author", "genre", "name")

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            self.permission_classes = (IsLibrarian,)
        return super().get_permissions()


class LendingListApiView(ListAPIView):
    def get_queryset(self):
        if IsLibrarian().has_permission(self.request, self):
            return Lending.objects.all()
        else:
            return Lending.objects.filter(user=self.request.user)

    serializer_class = LendingSerializer



class LendingCreateApiView(CreateAPIView):
    """Создавать могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_create(self, serializer):
        book_json_id = serializer.validated_data["book"].pk
        book_object = Books.objects.get(pk=book_json_id)
        lending = serializer.save()
        book_object.quantity_lending += 1
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
    serializer_class = LendingSerializer


class LendingUpdateApiView(UpdateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_update(self, serializer):
        book_json_id = serializer.validated_data["book"].pk
        book_object = Books.objects.get(pk=book_json_id)
        book_object.quantity_lending -= 1
        book_object.save()
        lending = serializer.save()
        lending.save()

    permission_classes = [IsLibrarian]


class LendingDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""

    def get_queryset(self):
        lending_object = Lending.objects.get(pk=self.kwargs['pk'])
        book_object = Books.objects.get(pk=lending_object.book_id)
        book_object.quantity_lending -= 1
        book_object.save()
            # if len(lending_object_list) == 1:
            #     if self.kwargs['pk'] != self.request.user.id:
            #         raise ValidationError(
            #             "У вас недостаточно прав на просмтр учетных данных читателя !"
            #         )
            #     return Users.objects.filter(pk=self.request.user.id)
            # else:
            #     raise ValidationError(
            #         "Такой читатель не зарегистрирован в библиотеке !"
            #     )
        return Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = [IsLibrarian]
