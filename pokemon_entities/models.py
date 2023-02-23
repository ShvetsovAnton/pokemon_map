from django.db import models


class Pokemon(models.Model):
    title = models.CharField('Имя покемона', max_length=200)
    photo = models.ImageField('Изображение покемона', blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Выберите покемона',
        on_delete=models.CASCADE)
    Lat = models.FloatField()
    Lon = models.FloatField()
