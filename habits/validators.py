from rest_framework.exceptions import ValidationError


def select_exception(attrs):
    if attrs.get("related") and attrs.get("reward"):
        raise ValidationError(
            f"В модели не должно быть заполнено одновременно и поле вознаграждения, и связанная привычка."
            f"Выберите что-то одно!"
        )


def estimated_time_validate(attrs):
    if attrs.get("estimated_time") > 120:
        raise ValidationError("Время выполнения должно быть не больше 120 секунд.")


def nice_habit_validate(attrs):
    if attrs.get("related") and not attrs.get("nice_habit"):
        raise ValidationError(
            f"В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )


def nice_habit_without_validate(attrs):
    if attrs.get("nice_habit") and attrs.get("reward") or attrs.get("related"):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def periodicity_validate(attrs):
    periodicity = attrs.get("periodicity")
    if not (1 <= periodicity <= 7):
        raise ValidationError(
            f"За одну неделю необходимо выполнить привычку хотя бы один раз."
        )
