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
    

class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name='Место')
    image = models.ImageField(verbose_name='Изображение')
    image_number = models.PositiveIntegerField(verbose_name='Номер изображения', default=0)

    def __str__(self):
        return f'{self.image_number} {self.place.title}'