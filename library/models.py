from datetime import date
from django.db import models
from config import settings

NULLABLE = {"blank": True, "null": True}


class Authors(models.Model):
    author = models.CharField(max_length=150, unique=True, verbose_name="имя (псевдоним) автора")
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

    name = models.CharField(max_length=150, unique=True, verbose_name="название книги")
    author = models.ForeignKey(
        Authors, related_name="book_author", on_delete=models.PROTECT, verbose_name="автор"
    )
    genre = models.CharField(max_length=20, choices=GENRE, verbose_name="жанр", default="story")
    annotation = models.TextField(verbose_name="аннотация", **NULLABLE)
    barcode = models.PositiveIntegerField(verbose_name="штрихкод", **NULLABLE)
    quantity_all = models.PositiveIntegerField(verbose_name="всего в библиотеке", default=0)
    quantity_lending = models.PositiveIntegerField(verbose_name="выдано всего", default=0)
    amount_lending = models.PositiveIntegerField(verbose_name="количество выдачи", default=0)
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
    OPERATION = [("arrival", "поступление"), ("issuance", "выдача"), ("return", "возврат"), ("loss", "утеря"), ("write_off", "списание")]

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
    operation = models.CharField(max_length=20, choices=OPERATION, verbose_name="операция", default="issuance")
    date_event = models.DateField(verbose_name="дата", default=date.today)

    id_return = models.IntegerField(verbose_name="id возврата", default=0)
    arrival_quantity = models.IntegerField(verbose_name="Количество поступивших книг.", **NULLABLE)

    def __str__(self):
        return f"{self.user} : {self.book}"

    class Meta:
        verbose_name = "выдача"
        verbose_name_plural = "выдачи"
