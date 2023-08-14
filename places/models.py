from django.db import models

# Create your models here.

class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description_short = models.TextField(verbose_name='Короткое описание')
    description_long = models.TextField(verbose_name='Описание')
    latitude = models.FloatField(verbose_name="Широта", null=True)
    longitude = models.FloatField(verbose_name="Долгота", null=True)

    def __str__(self):
        return self.title