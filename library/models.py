from datetime import date
from django.db import models
from config import settings

NULLABLE = {"blank": True, "null": True}


class Authors(models.Model):
    isni = models.CharField(max_length=16, unique=True, verbose_name="ISNI")
    author = models.CharField(max_length=150, verbose_name="имя (псевдоним) автора")
    image = models.ImageField(
        upload_to="authors/media",
        verbose_name="изображение",
        help_text="загрузите изображение автора",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def str(self):
        return f"Автор: {self.author}"


class Books(models.Model):
    GENRE = [("adventures", "приключения"), ("fantasy", "фантастика"),
                  ("story", "рассказ"), ("novel", "повесть"), ("poetry", "поэзия")]

    isbn = models.CharField(max_length=17, unique=True, verbose_name="ISBN")
    name = models.CharField(max_length=150, verbose_name="название книги")
    author = models.ForeignKey(
        Authors, related_name="book_author", on_delete=models.PROTECT, verbose_name="автор"
    )
    genre = models.CharField(max_length=20, choices=GENRE, verbose_name="жанр", default="story")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    barcode = models.PositiveIntegerField(verbose_name="штрихкод")
    quantity_all = models.PositiveIntegerField(verbose_name="всего в библиотеке")
    quantity_lending = models.PositiveIntegerField(verbose_name="выдано всего", default=0)
    image = models.ImageField(
        upload_to="books/media",
        verbose_name="обложка",
        help_text="загрузите обложку",
        **NULLABLE,
    )

    def str(self):
        return f"Книга: {self.name}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Lending(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="читатель",
        related_name="lending_user",
    )
    book = models.ForeignKey(
        Books,
        on_delete=models.PROTECT,
        verbose_name="книга",
        related_name="lending_book",
    )
    date_lending = models.DateField(verbose_name="дата выдачи", default=date.today)
    days = models.PositiveIntegerField(verbose_name="количество дней", default=10)
    date_return = models.DateField(verbose_name="дата возврата фактическая", **NULLABLE)

    def __str__(self):
        return f"{self.user} : {self.book}"

    class Meta:
        verbose_name = "выдача"
        verbose_name_plural = "выдачи"
