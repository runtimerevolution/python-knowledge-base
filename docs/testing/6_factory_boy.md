# Factory boy

<https://factoryboy.readthedocs.io/en/stable/index.html>

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

---

## Faker

- factory boy with faker <https://factoryboy.readthedocs.io/en/stable/reference.html#faker>
- faker <https://faker.readthedocs.io/en/latest/>

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
<https://faker.readthedocs.io/en/latest/providers/faker.providers.person.html#faker.providers.person.Provider.name>

### Faker attribute with params

Let's say we want our music durations to be between 30 and 500 seconds
we can use `random_int` like in
<https://faker.readthedocs.io/en/latest/providers/baseprovider.html#faker.providers.BaseProvider.random_int>

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

You can find more providers [here](https://faker.readthedocs.io/en/latest/providers.html). If you can't find the provider you need, you can also check [here](https://faker.readthedocs.io/en/latest/communityproviders.html) for community maintained providers.

If you still can't find the provider you need. You can always develop your own custom provider.

### Custom providers

You can very easily create your own custom Faker providers to supplement your factories with better, more revelant data. For example, let's say you want better names for the MusicTrack model instead of generating a person's name.

```python
import factory
from faker.providers import BaseProvider

class MusicTrackNameProvider(BaseProvider):
    __provider__ = "track_name"
    song_names_1 = [
        "The Awakening",
        "The Voyagers",
        "The Empyreal",
        "Of Carnage and",
        "Callisto",
        "The Scourge",
        "The Thirteen",
    ]
    song_names_2 = [
        "of the Stars",
        "Beneath the Mare Imbrium",
        "Lexicon",
        "a Gathering of the Wolves",
        "Rising",
        "of the Fourth Celestial Host",
        "Cryptical Prophecies of Mu",
    ]

    def track_name(self):
        return f"{self.random_element(self.track_names_1)} {self.random_element(self.track_names_2)}"

# This is the important bit that allows you to simply invoke the provider with the name "track_name".
factory.Faker.add_provider(MusicTrackNameProvider)

class MusicTrackFactory(factory.django.DjangoModelFactory):
    # Invoking the provider is as simple as calling the value defined in __provider__.
    name = factory.Faker("track_name")
```

As you can see, this is very simple to do and you can easily make your factories output data with higher quality. You can be as creative and versatile with the data that is generated as you need. For this example, it simply combines random values from two different lists.

For code-organization reasons, you can always implement your providers in a providers.py file and have your factories in the factories.py file.

---

## Relations and Foreign Keys

<https://factoryboy.readthedocs.io/en/stable/recipes.html#dependent-objects-foreignkey>

You can use SubFactory to create other dependent models like:

```python
class BandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')

class MusicTrackFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    Band = factory.SubFactory(BandFactory)
```

---

## Unique constraints

<https://factoryboy.readthedocs.io/en/stable/orms.html#factory.django.DjangoOptions.django_get_or_create>

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

---

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

---

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
