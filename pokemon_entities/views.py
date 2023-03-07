import folium

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.timezone import now
from .models import (Pokemon,
                     PokemonEntity)


MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon(folium_map, lat, lon, image_url):
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
    pokemons_on_page = []
    localtime = now()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_entities = PokemonEntity.objects.filter(
        appeared_at__lte=localtime,
        disappeared_at__gte=localtime
    )
    for entities in pokemons_entities:
        add_pokemon(
            folium_map, entities.lat,
            entities.lon,
            request.build_absolute_uri(entities.pokemon.photo.url)
        )
        pokemons_on_page.append({
            'pokemon_id': entities.pokemon.id,
            'img_url': request.build_absolute_uri(entities.pokemon.photo.url),
            'title_ru': entities.pokemon.title_ru,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    previous_evol_stage_pokemon = pokemon.previous_evolution
    next_evol_stage_pokemon = pokemon.next_evolutions.first()
    pokemon_description = {
        'pokemon_id': pokemon_id,
        'img_url': request.build_absolute_uri(
            pokemon.photo.url
        ),
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_eng,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description
    }
    if next_evol_stage_pokemon:
        pokemon_description.update(
            {
                'next_evolution': {
                    'title_ru': next_evol_stage_pokemon.title_ru,
                    'pokemon_id': next_evol_stage_pokemon.id,
                    'img_url': request.build_absolute_uri(
                        next_evol_stage_pokemon.photo.url
                    )
                }
            }
        )
    if previous_evol_stage_pokemon:
        pokemon_description.update(
            {
                'previous_evolution': {
                    'title_ru': previous_evol_stage_pokemon.title_ru,
                    'pokemon_id': previous_evol_stage_pokemon.id,
                    'img_url': request.build_absolute_uri(
                        previous_evol_stage_pokemon.photo.url
                    )
                }
            }
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_description
    })
