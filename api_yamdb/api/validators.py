import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserDataValidation:
    FORBIDDEN_NAME = 'me'

    def validate_username(self, username):

        if not re.match(pattern=r'[\w._@+-]+', string=username):
            raise ValidationError(
                'Введите корректное имя пользователя.'
                'Оно может содержать только буквы и символы @/./+/-/_. '
            )
        if username == self.FORBIDDEN_NAME:
            raise ValidationError(
                f'Использовать имя {self.FORBIDDEN_NAME} '
                'в качестве username запрещено.')
        return username

    def validate_email(self, email):
        try:
            validate_email(email)
        except Exception:
            raise ValidationError('Введен некорректный почтовый ящик')
        return email
