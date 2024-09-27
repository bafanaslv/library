from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from library.models import Authors, Books
from library.serializer import AuthorsSerializer
from users.permissions import IsLibrarian


class AuthorsViewSet(ModelViewSet):
    def get_queryset(self):
        return Authors.objects.all()

    serializer_class = AuthorsSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "retrieve", "destroy"]:
            self.permission_classes = (IsLibrarian, IsAuthenticated,)
        elif self.action == "list":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()


class BooksListApiView(ListAPIView):
    def get_queryset(self):
        return Books.objects.all()


