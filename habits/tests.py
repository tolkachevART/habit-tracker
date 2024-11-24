from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitsTestCase(APITestCase):
    """
    Тестовый класс для проверки функционала работы с привычками (Habits).
    """

    def setUp(self):
        """
        Настройка тестового окружения перед каждым тестовым методом.
        Создает пользователя, аутентифицирует клиента и создает две привычки.
        """
        self.user = User.objects.create(email="test@mail.com", password="test")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("habits:habit-list")

        self.habit = Habit.objects.create(
            owner=self.user,
            action="Зарядка",
            periodicity=2,
            location="Дом",
            time="09:00",
            estimated_time=120,
        )

        self.nice_habit = Habit.objects.create(
            owner=self.user,
            action="Выпить сок",
            periodicity=1,
            location="Дом",
            time="10:00",
            estimated_time=30,
            nice_habit=True,
            is_public=True,
        )

    def test_create_habit(self):
        """
        Проверяет создание новой привычки через API.
        Убедитесь, что новая привычка создается правильно и возвращается соответствующий статус-код.
        """
        data = {
            "action": "Приседания",
            "periodicity": 2,
            "location": "Спортзал",
            "time": "11:00",
            "estimated_time": 120,
            "nice_habit": False,
            "is_public": True,
            "reward": "Съесть яблоко",
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["action"], "Приседания")
        self.assertEqual(response.data["periodicity"], 2)
        self.assertIsNotNone(response.data["owner"])
        self.assertTrue(Habit.objects.filter(action="Приседания").exists())

    def test_list_habits(self):
        """
        Проверяет получение списка привычек через API.
        Убедиться, что возвращаются все созданные привычки и ответ имеет правильный статус-код.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_update_habit(self):
        """
        Проверяет обновление существующей привычки через API.
        Убедиться, что обновленные данные сохраняются и возвращаются правильные значения.
        """
        url = reverse("habits:habit-detail", args=[self.habit.pk])
        data = {
            "action": "Обновленная привычка",
            "periodicity": 1,
            "location": "Кафе",
            "time": "12:00",
            "estimated_time": 60,
            "nice_habit": False,
            "is_public": True,
            "reward": "Мотивация",
        }

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Обновленная привычка")

    def test_destroy_habit(self):
        """
        Проверяет удаление привычки через API.
        Убедиться, что привычка действительно удаляется и возвращается правильный статус-код.
        """
        url = reverse("habits:habit-detail", args=[self.habit.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())
