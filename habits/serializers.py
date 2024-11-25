from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import (
    select_exception,
    estimated_time_validate,
    nice_habit_validate,
    nice_habit_without_validate,
    periodicity_validate,
)


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("owner",)

    def validate(self, attrs):
        select_exception(attrs)
        estimated_time_validate(attrs)
        nice_habit_validate(attrs)
        nice_habit_without_validate(attrs)
        periodicity_validate(attrs)

        return attrs
