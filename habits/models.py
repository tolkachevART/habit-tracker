from django.db import models

from users.models import User


class Habit(models.Model):
    """
    Модель представляет собой привычку пользователя.
    Содержит информацию о владельце, времени, месте, частоте выполнения и других характеристиках привычки.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    location = models.CharField(max_length=255, verbose_name="Локация")
    time = models.TimeField(verbose_name="Время выполнения привычки")
    action = models.CharField(max_length=100, verbose_name="Активность")
    estimated_time = models.IntegerField(verbose_name="Время потраченное на выполнение (в секундах)")
    last_performed = models.DateField(null=True, blank=True, verbose_name='Дата последнего выполнения')
    periodicity = models.PositiveIntegerField(default=1, verbose_name='Интервал выполнения (дни)')
    nice_habit = models.BooleanField(default=True, verbose_name="Приятная привычка")
    is_public = models.BooleanField(default=False, verbose_name="Опубликована")
    related = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная с другой привычкой",
    )
    reward = models.CharField(max_length=100, null=True, blank=True, verbose_name="Вознаграждение")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.location}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-id"]
