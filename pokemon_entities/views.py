import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import now
from .models import (Pokemon,
                     PokemonEntity)


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def take_pokemon_entity(pokemon, request, folium_map):
    try:
        pokemon_entity = PokemonEntity.objects.get(pokemon=pokemon)
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.photo.url)
        )
    except PokemonEntity.DoesNotExist:
        raise PokemonEntity.DoesNotExist(
            f'Для покемона - {pokemon} не заданны координаты.'
        )
    except PokemonEntity.MultipleObjectsReturned:
        raise PokemonEntity.MultipleObjectsReturned(
            'Кажется покемонов несколько.'
        )


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.exclude(photo=None).filter(
        appear__lte=now(),
        disappear__gte=now()
    ).select_related()
    for pokemon in pokemons:
        take_pokemon_entity(pokemon, request, folium_map)
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
        take_pokemon_entity(pokemon, request, folium_map)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': {
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
            "title_en": "Venusaur",
            "title_jp": "フシギバナ",
            'description': pokemon.description
        }
    })

