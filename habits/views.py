from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginations import HabitPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    """
    ViewSet для управления моделями Habit.
    Реализует CRUD-функционал для создания, получения, обновления и удаления привычек.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def perform_create(self, serializer):
        """
        Создает новую запись в базе данных.
        """
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Устанавливает права доступа в зависимости от действия.
        """
        if self.action == "create":
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "destroy"]:
            self.permission_classes = (IsOwner,)
        elif self.action == "list":
            self.permission_classes = (IsAuthenticated,)
        elif self.action == "retrieve":
            self.permission_classes = (IsOwner | IsAuthenticated,)
        return super().get_permissions()

    def get_queryset(self):
        """
        Получает список привыечек, доступных для просмотра текущему пользователю.
        """
        if self.action == "list":
            return Habit.objects.filter(is_public=True) | Habit.objects.filter(
                owner=self.request.user
            )
        return super().get_queryset()
