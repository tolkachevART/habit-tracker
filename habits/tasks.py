from datetime import timedelta

import pytz
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from telebot import logger

from habits.models import Habit
from habits.services import send_telegram_message

# Добавляем список дней недели для удобства работы с ними
DAYS_OF_WEEK = [
    'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'
]


@shared_task()
def telegram_notification():
    zone = pytz.timezone(settings.TIME_ZONE)
    now = timezone.now().astimezone(zone)

    # Получаем текущее время с учетом зоны
    current_time = now.time()
    current_time_less = (now - timedelta(minutes=5)).time()

    # Получаем текущий день недели
    today = DAYS_OF_WEEK[now.weekday()]

    # Фильтрация привычек по времени и периодичности
    habits = Habit.objects.filter(
        time__gte=current_time_less,
        time__lte=current_time
    ).select_related('owner')  # Используем select_related для оптимизации запросов к базе данных

    for habit in habits:
        if habit.periodicity == True or (habit.periodicity == False and today == habit.day_of_week):
            try:
                user_tg = habit.owner.tg_chat_id
                message = f"Я буду {habit.action} в {habit.time} в {habit.location}"
                send_telegram_message(user_tg, message)

                # Логируем успешное уведомление
                logger.info(f"Успешно отправлено уведомление пользователю {habit.owner}: {message}")
            except Exception as e:
                # Логируем ошибку
                logger.error(f"Ошибка при отправке уведомления пользователю {habit.owner}: {e}")
