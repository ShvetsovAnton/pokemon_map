from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Из кого эволюционировал',
        on_delete=models.CASCADE,
        related_name='next_evolutions',
        blank=True,
        null=True
    )
    title_ru = models.CharField(
        'Имя покемона RU',
        max_length=200
    )
    title_eng = models.CharField(
        'Имя покемона ENG',
        blank=True,
        max_length=200
    )
    title_jp = models.CharField(
        'Имя покемона JP',
        blank=True,
        max_length=200
    )
    photo = models.ImageField('Изображение покемона')
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """Координаты покемонов, привязаны к покемону"""
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Выберите покемона',
        related_name='entities',
        on_delete=models.SET_NULL,
        null=True
    )
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Появиться')
    disappeared_at = models.DateTimeField('Исчезнет')
    level = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    strength = models.IntegerField('Атака', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)

    def __str__(self):
        return f'Информация о покемоне {self.pokemon.title_ru}'
