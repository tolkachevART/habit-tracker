from datetime import timedelta

import pytz
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from telebot import logger

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task()
def telegram_notification():
    zone = pytz.timezone(settings.TIME_ZONE)
    now = timezone.now().astimezone(zone)

    # Получаем текущее время с учетом зоны
    current_time = now.time()
    current_time_less = (now - timedelta(minutes=5)).time()

    # Фильтруем привычки по времени
    habits = Habit.objects.filter(time__range=(current_time_less, current_time))

    for habit in habits:
        try:
            user_tg = habit.owner.tg_chat_id
            message = f"Я буду {habit.action} в {habit.time} в {habit.location}"
            send_telegram_message(user_tg, message)

            # Логируем успешное уведомление
            logger.info(f"Успешно отправлено уведомление пользователю {habit.owner}: {message}")
        except Exception as e:
            # Логируем ошибку
            logger.error(f"Ошибка при отправке уведомления пользователю {habit.owner}: {e}")
