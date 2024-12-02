
import string
import random
from .models import User


def generate_invite_code():
    """
    Вспомогательная функция для генерации инвайт-кода для нового юзера
    """
    while True:
        new_invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        # если найдется юзер с таким кодом - продолжаем генерировать новые
        if User.objects.filter(invite_code=new_invite_code).exists():
            continue
        else:
            return new_invite_code

