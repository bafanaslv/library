from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Courses, Lessons

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail")
    phone = models.CharField(max_length=15, verbose_name="Телефон", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="Город", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"


class Payments(models.Model):
    METHOD = [("cache", "наличными"), ("transfer", "перевод")]

    user = models.ForeignKey(
        User,
        related_name="users",
        on_delete=models.PROTECT,
        verbose_name="пользователь",
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name="дата оплаты")
    paid_course = models.ForeignKey(
        Courses,
        related_name="paid_course",
        on_delete=models.PROTECT,
        verbose_name="оплаченный курс",
        **NULLABLE,
    )
    paid_lesson = models.ForeignKey(
        Lessons,
        related_name="paid_lesson",
        on_delete=models.PROTECT,
        verbose_name="оплаченный урок",
        **NULLABLE,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="cумма оплаты"
    )
    payment_method = models.CharField(
        max_length=10, choices=METHOD, verbose_name="способ оплаты"
    )
    session_id = models.CharField(max_length=255, verbose_name="Id сессии", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="Cсылка на оплату", **NULLABLE)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def str(self):
        if self.paid_course is not None:
            course_or_lesson = "за курс"
        else:
            course_or_lesson = "за урок"
        return f"Оплата за {course_or_lesson}, дата оплаты: {self.payment_date}, сумма: {self.payment_method}, способ: {self.payment_method}"
