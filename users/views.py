# Описание представления не требует детелизации. Здесь все стандартно.

from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from library.models import Lending
from users.models import Users
from users.permissions import IsLibrarian
from users.serializer import UserSerializer, UserTokenObtainPairSerializer


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = [IsAuthenticated, IsLibrarian]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if IsLibrarian().has_permission(self.request, self):
            return Users.objects.all()
        else:
            lending_object_list = list(Users.objects.filter(pk=self.kwargs["pk"]))
            if len(lending_object_list) == 1:
                if self.kwargs["pk"] != self.request.user.id:
                    raise ValidationError(
                        "У вас недостаточно прав на просмтр учетных данных читателя !"
                    )
                return Users.objects.filter(pk=self.request.user.id)
            else:
                raise ValidationError(
                    "Такой читатель не зарегистрирован в библиотеке !"
                )

    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        lending_object_list = list(Users.objects.filter(pk=self.kwargs["pk"]))
        if len(lending_object_list) == 1:
            if self.kwargs["pk"] != self.request.user.id:
                raise ValidationError(
                    "У вас недостаточно прав на изменение учетных данных читателя !"
                )
            return Users.objects.filter(pk=self.request.user.id)
        else:
            raise ValidationError("Такой читатель не зарегистрирован в библиотеке !")

    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()


class UserDestroyAPIView(DestroyAPIView):
    def get_queryset(self):
        lending_object_list = list(Lending.objects.filter(user=self.request.user.id))
        if len(lending_object_list) > 0:
            raise ValidationError(
                "Невозможно удалить читателя, который пользовался услугами библиотеки !"
            )
        else:
            lending_object_list = list(Users.objects.filter(pk=self.kwargs["pk"]))
            if len(lending_object_list) == 0:
                raise ValidationError(
                    "Такой читатель не зарегистрирован в библиотеке !"
                )
            return Users.objects.all()

    permission_classes = [IsAuthenticated, IsLibrarian]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(self.request.data.get("password"))
        user.save()


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
