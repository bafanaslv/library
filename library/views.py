from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from library.models import Authors, Books, Lending
from library.serializer import AuthorsSerializer, BooksSerializer, LendingSerializer
from users.permissions import IsLibrarian


class AuthorsListApiView(ListAPIView):
    serializer_class = AuthorsSerializer
    queryset = Authors.objects.all()


class AuthorsCreateApiView(CreateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer

    def perform_create(self, serializer):
        authors = serializer.save()
        authors.save()

    permission_classes = [IsAuthenticated, IsLibrarian]


class AuthorsRetrieveApiView(RetrieveAPIView):
    """Просматривать отдельного могут авторизованный пользователь, который является владельцем или модератором."""

    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer

    permission_classes = [AllowAny]


class AuthorsUpdateApiView(UpdateAPIView):
    """Создавать могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer

    def perform_update(self, serializer):
        author = serializer.save()
        author.save()

    permission_classes = [IsAuthenticated, IsLibrarian]


class AuthorsDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]


class BooksListApiView(ListAPIView):
    serializer_class = BooksSerializer
    queryset = Books.objects.all()
    permission_classes = [AllowAny]


class BooksCreateApiView(CreateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def perform_create(self, serializer):
        books = serializer.save()
        books.save()

    permission_classes = [IsAuthenticated, IsLibrarian]


class BooksRetrieveApiView(RetrieveAPIView):
    """Просматривать отдельного могут авторизованный пользователь, который является владельцем или модератором."""

    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    permission_classes = [AllowAny]


class BooksUpdateApiView(UpdateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def perform_update(self, serializer):
        books = serializer.save()
        books.save()

    permission_classes = [IsAuthenticated, IsLibrarian]


class BooksDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]


class LendingListApiView(ListAPIView):
    serializer_class = LendingSerializer
    queryset = Lending.objects.all()
    permission_classes = [AllowAny]


class LendingCreateApiView(CreateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Lending.objects.all()
    serializer_class = BooksSerializer

    def perform_create(self, serializer):
        lending = serializer.save()
        lending.save()

    permission_classes = [IsAuthenticated, IsLibrarian]


class LendingRetrieveApiView(RetrieveAPIView):
    """Просматривать отдельного могут авторизованный пользователь, который является владельцем или модератором."""

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    permission_classes = [AllowAny]


class LendingUpdateApiView(UpdateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_update(self, serializer):
        lending = serializer.save()
        lending.save()

    permission_classes = [IsAuthenticated, IsLibrarian]


class LendingDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]

