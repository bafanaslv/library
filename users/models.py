# В проекте предусмотрены два типа пользователей. Библиотекарь, обладающий всеми правами и читатель, который может
# проматривать авторов, списки и аннотации книг и разного рода информацию по полученным им книгам.
# Библиотекарь входит в группу librarian, через которого получает все права в приложении.

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Users(AbstractUser):
    username = None
    reader_name = models.CharField(max_length=50, verbose_name="ФИО читателя")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    is_personal_data = models.BooleanField(
        default=True, verbose_name="Согласие на обработку персональных данных"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", **NULLABLE
    )
    tg_chat_id = models.CharField(
        max_length=50, verbose_name="Telergram chat_id", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"
