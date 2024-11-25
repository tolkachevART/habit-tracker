from django.contrib.auth.models import AbstractUser
from django.db import models

from nullable import NULLABLE


class User(AbstractUser):
    """
    Модель пользователя, расширяющая стандартную модель Django Auth.
    В этой модели используется электронная почта вместо имени пользователя для входа,
    а также добавляются дополнительные поля, такие как телефон, аватар, город и Telegram Chat ID.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", **NULLABLE
    )
    city = models.CharField(max_length=100, verbose_name="Город", **NULLABLE)
    tg_chat_id = models.CharField(
        max_length=100, verbose_name="Телеграм chat_id", **NULLABLE
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
