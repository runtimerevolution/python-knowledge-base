from django.utils import timezone
from datetime import timedelta


def yesterday():
    dt = timezone.now() + timedelta(days=-1)
    return dt.date()
