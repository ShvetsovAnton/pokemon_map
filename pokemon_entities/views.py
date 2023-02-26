import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import now
from .models import (Pokemon,
                     PokemonEntity)


MOSCOW_CENTER = [55.751244, 37.618423]


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
            'Кажется у этой особи несколько координат.'
        )


def take_pokemon_description(request, pokemon):
    try:
        previous_evolution_stage = pokemon.previous_evolution
        next_evolutions_stage = pokemon.next_evolutions.get(
            previous_evolution=pokemon
        )
        pokemon_description = {
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
            "title_en": pokemon.title_eng,
            "title_jp": pokemon.title_jp,
            'description': pokemon.description,
            "previous_evolution": {
                "title_ru": previous_evolution_stage.title,
                "pokemon_id": previous_evolution_stage.id,
                "img_url": request.build_absolute_uri(
                    previous_evolution_stage.photo.url
                )
            },
            "next_evolution": {
                "title_ru": next_evolutions_stage.title,
                "pokemon_id": next_evolutions_stage.id,
                "img_url": request.build_absolute_uri(
                    next_evolutions_stage.photo.url
                )
            }
        }
    except AttributeError:
        try:
            pokemon_description = {
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.photo.url),
                'title_ru': pokemon.title,
                "title_en": pokemon.title_eng,
                "title_jp": pokemon.title_jp,
                'description': pokemon.description,
                "next_evolution": {
                    "title_ru": next_evolutions_stage.title,
                    "pokemon_id": next_evolutions_stage.id,
                    "img_url": request.build_absolute_uri(
                        next_evolutions_stage.photo.url
                    )
                }
            }
        except AttributeError:
            pokemon_description = {
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.photo.url),
                'title_ru': pokemon.title,
                "title_en": pokemon.title_eng,
                "title_jp": pokemon.title_jp,
                'description': pokemon.description
            }
            return pokemon_description
    except Pokemon.DoesNotExist:
        try:
            pokemon_description = {
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.photo.url),
                'title_ru': pokemon.title,
                "title_en": pokemon.title_eng,
                "title_jp": pokemon.title_jp,
                'description': pokemon.description,
                "previous_evolution": {
                    "title_ru": previous_evolution_stage.title,
                    "pokemon_id": previous_evolution_stage.id,
                    "img_url": request.build_absolute_uri(
                        previous_evolution_stage.photo.url
                    )
                }
            }
        except AttributeError:
            pokemon_description = {
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.photo.url),
                'title_ru': pokemon.title,
                "title_en": pokemon.title_eng,
                "title_jp": pokemon.title_jp,
                'description': pokemon.description
            }
            return pokemon_description
    except Pokemon.MultipleObjectsReturned:
        raise Pokemon.MultipleObjectsReturned(
            'Покемон может эволюционировать только в одну особь.'
            'Проверьте базу данных'
        )
    return pokemon_description


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
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_with_image = Pokemon.objects.filter(
        appear__lte=now(),
        disappear__gte=now()
    ).select_related()
    for pokemon in pokemons_with_image:
        print(pokemon)
        take_pokemon_entity(pokemon, request, folium_map)
    for pokemon in pokemons_with_image:
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
    pokemon_description = take_pokemon_description(request, pokemon)
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_description
    })
