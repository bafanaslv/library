from rest_framework import viewsets
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

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
        lending = serializer.save()
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
        lending = serializer.save()
        lending.save()

    permission_classes = [IsLibrarian]


class LendingDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = [IsLibrarian]
