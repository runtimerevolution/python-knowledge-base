from django.db import models


class Animal(models.Model):
    name = models.TextField()
    sound = models.TextField()

    def speak(self):
        return f'The {self.name} says "{self.sound}"'
