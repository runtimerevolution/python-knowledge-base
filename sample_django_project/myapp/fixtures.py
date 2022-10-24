import pytest
from .models import Animal


@pytest.fixture(scope="function")
def cat():
    Animal.objects.create(name="cat", sound="meow")


@pytest.fixture(scope="function")
def lion():
    Animal.objects.create(name="lion", sound="roar")


@pytest.fixture(scope="function")
def felines(lion, cat):
    ...