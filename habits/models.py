from django.db import models

from nullable import NULLABLE
from users.models import User


class Habit(models.Model):
    """
    Модель представляет собой привычку пользователя.
    Содержит информацию о владельце, времени, месте, частоте выполнения и других характеристиках привычки.
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    location = models.CharField(
        max_length=255,
        verbose_name="Локация",
        help_text="Укажите локацию, в которой необходимо выполнять привычку",
    )
    time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Время выполнения привычки",
        help_text="Установите время, когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=100,
        verbose_name="Активность",
        help_text="Укажите действие, которое нужно совершить",
    )
    estimated_time = models.IntegerField(
        verbose_name="Время потраченное на выполнение (в секундах)"
    )
    periodicity = models.IntegerField(
        default=1,
        verbose_name="Периодичность в днях",
        help_text="Укажите периодичность выполнения привычки в днях (по умолчанию ежедневная)",
    )
    nice_habit = models.BooleanField(
        default=True, verbose_name="Приятная привычка", **NULLABLE
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Опубликована", **NULLABLE
    )
    related = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная с другой привычкой",
        **NULLABLE,
    )
    reward = models.CharField(max_length=100, verbose_name="Вознаграждение", **NULLABLE)

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.location}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-id"]
