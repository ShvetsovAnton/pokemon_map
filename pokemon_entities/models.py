from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    Lat = models.FloatField()
    Lon = models.FloatField()
