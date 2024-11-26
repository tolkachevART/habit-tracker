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

    # Получаем текущую дату
    today = now.date()

    # Фильтрация привычек по времени и дате последнего выполнения
    habits = Habit.objects.filter(
        time__gte=current_time_less,
        time__lte=current_time
    ).select_related('owner')

    for habit in habits:
        if habit.last_performed:
            next_action_date = habit.last_performed + timedelta(days=habit.periodicity)

            if next_action_date > today:
                continue

        try:
            user_tg = habit.owner.tg_chat_id
            message = f"Я буду {habit.action} в {habit.time} в {habit.location}"
            send_telegram_message(user_tg, message)

            # Обновляем дату последнего выполнения
            habit.last_performed = today
            habit.save()

            # Логируем успешное уведомление
            logger.info(f"Успешно отправлено уведомление пользователю {habit.owner}: {message}")
        except Exception as e:
            # Логируем ошибку
            logger.error(f"Ошибка при отправке уведомления пользователю {habit.owner}: {e}")
