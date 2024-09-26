from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from library.models import Authors
from library.serializer import AuthorsSerializer
from users.permissions import IsModerator, IsOwner


class AuthorsViewSet(ModelViewSet):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Authors.objects.all()
        else:
            return Authors.objects.filter(owner=self.request.user)

    serializer_class = AuthorsSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModerator | IsOwner,
            )
        return super().get_permissions()


class BooksListApiView(ListAPIView):
    pass
