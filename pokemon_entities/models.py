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
        max_length=200,
        null=False
    )
    title_eng = models.CharField(
        'Имя покемона ENG',
        max_length=200,
        null=False
    )
    title_jp = models.CharField(
        'Имя покемона JP',
        max_length=200,
        null=False
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """Координаты покемонов, привязаны к покемону"""
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Выберите покемона',
        related_name='pokemon_entity',
        on_delete=models.CASCADE)
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    photo = models.ImageField('Изображение покемона')
    appear_at = models.DateTimeField('Появиться')
    disappear_at = models.DateTimeField('Исчезнет')
    leve = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    strength = models.IntegerField('Атака', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=False)

    def __str__(self):
        return f'Информация о покемоне: {self.pokemon}'
