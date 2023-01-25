# Factory boy

https://factoryboy.readthedocs.io/en/stable/index.html

As a fixtures replacement tool, it aims to replace static, hard to maintain fixtures with easy-to-use factories for
complex objects.

This is a simple how to guide for how to use this library:

## Django models

Let's consider we have the following django models:

```python
class MusicTrack(models.Model):
    name = models.TextField()
    duration = models.IntegerField() # in seconds
    band = models.ForeignKey(Band, on_delete=models.DO_NOTHING)
    release_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = ["name", "band"]

class Band(models.Model):
    name = models.TextField()
    custom_id = models.TextField(unique=True)
```

## Faker

- factory boy with faker https://factoryboy.readthedocs.io/en/stable/reference.html#faker
- faker https://faker.readthedocs.io/en/latest/

Factory boy has many ways to generate data, usually we prefer to use Faker,
factory boy provides a wrapper for faker

### Simple faker attribute

```python
class MusicTrackFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = MusicTrack
```

Basically this is calling the `name` function in Faker library
https://faker.readthedocs.io/en/latest/providers/faker.providers.person.html#faker.providers.person.Provider.name

### Faker attribute with params

Let's say we want our music durations to be between 30 and 500 seconds
we can use `random_int` like in
https://faker.readthedocs.io/en/latest/providers/baseprovider.html#faker.providers.BaseProvider.random_int

:x: **Common Mistake:**

```python
class MusicTrackFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    duration = fake.random_int(min=30, max=500)
```

the issue with the implementation above is that it will generate a random number only once.

For example, when you would run a `MusicTrackFactory.create()` the duration would be some random number like 154,
and the next time you run `MusicTrackFactory.create()` the duration would all be 154, instead of a new random number

:white_check_mark: **Correct Implementation:**

```python
class MusicTrackFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    duration = factory.Faker('random_int',min=30, max=500)
```

### Other providers

Here is a list of other fakers classes https://faker.readthedocs.io/en/latest/providers.html

## Relations and Foreign Keys

https://factoryboy.readthedocs.io/en/stable/recipes.html#dependent-objects-foreignkey

You can use SubFactory to create other dependent models like:

```python
class BandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')

class MusicTrackFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    Band = factory.SubFactory(BandFactory)
```

## Unique constraints

https://factoryboy.readthedocs.io/en/stable/orms.html#factory.django.DjangoOptions.django_get_or_create

for django we use django_get_or_create, for unique fields so we don't have exception when running tests

```python
class BandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    custom_id = factory.Faker("lexify", text="???-###-????????-????")

    class Meta:
        model = Band
        django_get_or_create = ("custom_id",)

class MusicTrackFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    band = factory.SubFactory(BandFactory)

    class Meta:
        model = MusicTrack
        django_get_or_create = ("name","band",)
```

## Final Factories

```python
class BandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    custom_id = factory.Faker("lexify", text="???-###-????????-????")

    class Meta:
        model = Band
        django_get_or_create = ("custom_id",)

class MusicTrackFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    band = factory.SubFactory(BandFactory)
    release_date = factory.Faker('date_this_century',before_today=True)
    duration = factory.Faker('random_int',min=30, max=500)
    class Meta:
        model = MusicTrack
        django_get_or_create = ("name","band",)
```

## If conditions within Factory (factory.Maybe Method)

Let's consider the following Factory example:

```python
class BandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    custom_id = factory.Faker("lexify", text="???-###-????????-????")
    pseudonym = factory.Faker("boolean", chance_of_getting_true=0)
    band = factory.Maybe(
        "pseudonym",
        yes_declaration=factory.SubFactory("<project_name>.factories.BandFactory", pseudonym=False),
        no_declaration=None,
    )
```

In this example the attribute `band` will only be not null if the `pseudonym` attribute (which is a boolean field) has a value of true.
To implement this we can use the `factory.Maybe` Method.
