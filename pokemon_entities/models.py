from django.db import models


class Pokemon(models.Model):
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Из кого эволюционировал',
        on_delete=models.CASCADE,
        related_name='next_evolutions',
        null=True,
        blank=True
    )
    title = models.CharField('Имя покемона RU', max_length=200, default='')
    title_eng = models.CharField('Имя покемона ENG', max_length=200, default='')
    title_jp = models.CharField('Имя покемона JP', max_length=200, default='')
    photo = models.ImageField('Изображение покемона', blank=True, default=None)
    appear = models.DateTimeField('Появиться', blank=True, null=True)
    disappear = models.DateTimeField('Исчезнет', blank=True, null=True)
    leve = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    strength = models.IntegerField('Атака', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Выберите покемона',
        on_delete=models.CASCADE)
    lat = models.FloatField('Широта', blank=True)
    lon = models.FloatField('Долгота', blank=True)
