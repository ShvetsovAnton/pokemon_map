from django.db import models


class Pokemon(models.Model):
    title = models.CharField('Имя покемона', max_length=200)
    photo = models.ImageField('Изображение покемона', blank=True)
    appear = models.DateTimeField('Появиться', blank=True, null=True)
    disappear = models.DateTimeField('Исчезнет', blank=True, null=True)
    leve = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    strength = models.IntegerField('Атака', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Выберите покемона',
        on_delete=models.CASCADE)
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
