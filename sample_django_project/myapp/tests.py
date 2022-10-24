import pytest
from .fixtures import felines, lion, cat
from .models import Animal


@pytest.mark.django_db
def test_animals_can_speak(felines):
    """Animals that can speak are correctly identified"""
    lion = Animal.objects.get(name="lion")
    cat = Animal.objects.get(name="cat")

    assert lion.speak() == 'The lion says "roar"'
    assert cat.speak(), 'The cat says "meow"'

