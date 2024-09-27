from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from library.models import Authors, Books
from library.serializer import AuthorsSerializer, BooksSerializer
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


class AuthorsUpdateApiView(CreateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer

    def perform_create(self, serializer):
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


class BooksUpdateApiView(CreateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def perform_create(self, serializer):
        books = serializer.save()
        books.save()

    permission_classes = [IsAuthenticated, IsLibrarian]


class BooksDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]
