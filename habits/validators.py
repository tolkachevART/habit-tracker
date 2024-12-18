from rest_framework.exceptions import ValidationError


def select_exception(attrs):
    """
    Проверяет, что в атрибутах не заполнены одновременно поля 'related' и 'reward'.
    """
    if attrs.get("related") and attrs.get("reward"):
        raise ValidationError(
            "В модели не должно быть заполнено одновременно "
            "и поле вознаграждения, и связанная привычка."
            "Выберите что-то одно!"
        )


def estimated_time_validate(attrs):
    """
    Проверяет, что время выполнения привычки не превышает 120 секунд.
    """
    if attrs.get("estimated_time") > 120:
        raise ValidationError("Время выполнения должно быть не "
                              "больше 120 секунд.")


def nice_habit_validate(attrs):
    """
    Проверяет, что связанная привычка является приятной привычкой.
    """
    related_habit = attrs.get("related")
    if related_habit and not related_habit.nice_habit:
        raise ValidationError("Связанные привычки являются "
                              "приятными привычками.")


def nice_habit_without_validate(attrs):
    """
    Проверяет, что у приятной привычки нет вознаграждения или связанной привычки.
    """
    if attrs.get("nice_habit") and attrs.get("reward") or attrs.get("related"):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения "
            "или связанной привычки."
        )


def periodicity_validate(attrs):
    """
        Проверяет, что периодичность выполнения привычки находится в пределах от 1 до 7 дней.
    """
    periodicity = attrs.get("periodicity")
    if not (1 <= periodicity <= 7):
        raise ValidationError(
            "За одну неделю необходимо выполнить привычку хотя бы один раз."
        )
