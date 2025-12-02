import secrets

from rest_framework.serializers import ValidationError

from .models import (
    Link, )


def generate_unique_shortcode(token_len=8, max_retries=5):
    for _ in range(max_retries):
        code = secrets.token_urlsafe(token_len)
        print(code)
        if not Link.objects.filter(short_code=code).exists():
            return code
    raise ValidationError({'detail': 'Could not create code. Try again'})
