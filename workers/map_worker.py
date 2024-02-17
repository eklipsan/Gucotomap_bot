"""
This code defines classes and functions to work with map data.
It includes functions to randomly choose a town,
retrieve a map based on given coordinates,
and generate a set of countries for a quiz setup.
"""

import random
import json
from environs import Env
import requests
from dataclasses import dataclass
from typing import Union
from workers.logset import logger

@dataclass
class ChosenTown:
    town_name: str
    town_values: dict


@dataclass
class MapBox:
    url_link: str
    invalid_response: bool = False


def _receive_random_town() -> ChosenTown:
    """
    Retrieves a random town from a JSON file containing town data.
    """
    with open('map_data/towns.json', encoding='utf-8') as towns:
        json_file = json.load(towns)

    choice_town: str = random.choice(list(json_file.keys()))
    choice_values: dict[str: str] = json_file[choice_town]
    chosen_town: ChosenTown = ChosenTown(choice_town, choice_values)
    logger.debug("Retriving a random town from a JSON file")
    return chosen_town


def _receive_map(longtitude: str,
                 latitude: str,
                 lang: str = 'en_US',
                 scale: int = 1,
                 size: int = 11
                 ) -> MapBox:
    """
    Retrieves a map based on given coordinates and other optional parameters.
    """
    env = Env()
    env.read_env()
    form = r"https://static-maps.yandex.ru/v1?"
    url_link = f"{form}lang={lang}&ll={longtitude},{latitude}&scale={scale}&z={size}&size=650,450&apikey={env('API_KEY_MAP')}"

    map_box = MapBox(url_link=url_link)

    if requests.get(url_link).status_code == 200:
        logger.debug("Retriving a map based on given coordinates")
        return map_box
    else:
        map_box.invalid_response = True
        logger.error(f"Invalid response from the static maps server {map_box}")
        return map_box


def _receive_countries_set(right_country: str) -> tuple:
    """
    Generates a set of countries for a quiz setup,
    including the correct country and three random wrong countries.
    """
    with open('map_data/towns.json', encoding='utf-8') as js:
        json_file = json.load(js)

    countries_list: list[str] = [i['country']
                                 for i in list(json_file.values())]
    result_keyboard_set = set()
    result_keyboard_set.add(right_country)
    while len(result_keyboard_set) < 4:
        wrong_country = random.choice(countries_list)
        result_keyboard_set.add(wrong_country)
    logger.debug(f"Generating a set of countries for a quiz setup")
    return tuple(result_keyboard_set)


def receive_quiz_setup() -> Union[ChosenTown, MapBox, tuple[str]]:
    """
    Retrieves a random town, a map, and a set of countries for a quiz setup.
    """
    town = _receive_random_town()
    map = _receive_map(
        longtitude=town.town_values['longtitude'],
        latitude=town.town_values['latitude']
    )
    countries = _receive_countries_set(town.town_values['country'])
    logger.debug("Retriving a random town, its map, and a set of countries")

    return town, map, countries
