from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "destroy"]:
            self.permission_classes = (IsOwner,)
        elif self.action == "list":
            self.permission_classes = (IsAuthenticated,)
        elif self.action == "retrieve":
            self.permission_classes = (IsOwner | IsAuthenticated)
        return super().get_permissions()

    def get_queryset(self):
        if self.action == "list":
            return Habit.objects.filter(is_public=True) | Habit.objects.filter(owner=self.request.user)
        return super().get_queryset()
