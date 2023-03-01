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
    active_pokemons = Pokemon.objects.filter(
        pokemon_entity__appear_at__lte=localtime,
        pokemon_entity__disappear_at__gte=localtime
    ).select_related()
    for pokemon in active_pokemons:
        pokemon_entity = pokemon.pokemon_entity.first()
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.photo.url)
        )
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon_entity.photo.url),
            'title_ru': pokemon.title_ru,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entity = get_object_or_404(PokemonEntity, pokemon=pokemon_id)
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    previous_evol_stage_pokemon = pokemon.previous_evolution
    next_evol_stage_pokemon = pokemon.next_evolutions.first()
    previous_stage_pokemon_entity = PokemonEntity.objects.filter(
        pokemon=previous_evol_stage_pokemon
    ).first()

    next_evol_stage_pokemon_entity = PokemonEntity.objects.filter(
        pokemon=next_evol_stage_pokemon
    ).first()
    if next_evol_stage_pokemon and previous_evol_stage_pokemon:
        pokemon_description = {
            'pokemon_id': pokemon_id,
            'img_url': request.build_absolute_uri(
                pokemon_entity.photo.url
            ),
            'title_ru': pokemon_entity.pokemon.title_ru,
            'title_en': pokemon_entity.pokemon.title_eng,
            'title_jp': pokemon_entity.pokemon.title_jp,
            'description': pokemon_entity.description,
            'previous_evolution': {
                'title_ru': previous_evol_stage_pokemon.title_ru,
                'pokemon_id': previous_evol_stage_pokemon.id,
                'img_url': request.build_absolute_uri(
                    previous_stage_pokemon_entity.photo.url
                )
            },
            'next_evolution': {
                'title_ru': next_evol_stage_pokemon.title_ru,
                'pokemon_id': next_evol_stage_pokemon.id,
                'img_url': request.build_absolute_uri(
                    next_evol_stage_pokemon_entity.photo.url
                )
            }
        }
    if next_evol_stage_pokemon and not previous_evol_stage_pokemon:
        pokemon_description = {
            'pokemon_id': pokemon_id,
            'img_url': request.build_absolute_uri(
                pokemon_entity.photo.url
            ),
            'title_ru': pokemon_entity.pokemon.title_ru,
            'title_en': pokemon_entity.pokemon.title_eng,
            'title_jp': pokemon_entity.pokemon.title_jp,
            'description': pokemon_entity.description,
            'next_evolution': {
                'title_ru': next_evol_stage_pokemon.title_ru,
                'pokemon_id': next_evol_stage_pokemon.id,
                'img_url': request.build_absolute_uri(
                    next_evol_stage_pokemon_entity.photo.url
                )
            }
        }
    if previous_evol_stage_pokemon and not next_evol_stage_pokemon:
        pokemon_description = {
            'pokemon_id': pokemon_id,
            'img_url': request.build_absolute_uri(
                pokemon_entity.photo.url
            ),
            'title_ru': pokemon_entity.pokemon.title_ru,
            'title_en': pokemon_entity.pokemon.title_eng,
            'title_jp': pokemon_entity.pokemon.title_jp,
            'description': pokemon_entity.description,
            'previous_evolution': {
                'title_ru': previous_evol_stage_pokemon.title_ru,
                'pokemon_id': previous_evol_stage_pokemon.id,
                'img_url': request.build_absolute_uri(
                    previous_stage_pokemon_entity.photo.url
                )
            }
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_description
    })
