from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    """
    Класс для пагинации привычек.
    Наследуется от PageNumberPagination и устанавливает размер страницы равным 5.
    """
    page_size = 5
