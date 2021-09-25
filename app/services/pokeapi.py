from http import HTTPStatus

import requests
from fastapi import HTTPException
from requests import HTTPError

from app.config import POKEAPI_SPECIES_URL, POKEMON_NOT_FOUND, EXTERNAL_API_FAILED
from app.models import Pokemon


def get_pokemon(name: str) -> Pokemon:
    try:
        response = requests.get(f'{POKEAPI_SPECIES_URL}/{name}/')
        response.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == HTTPStatus.NOT_FOUND:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=POKEMON_NOT_FOUND)
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=EXTERNAL_API_FAILED)

    json = response.json()

    return Pokemon(name=json['name'],
                   description=json['flavor_text_entries'][0]['flavor_text'].replace('\n', ' ').replace('\x0c', ' '),
                   habitat=json['habitat']['name'],
                   isLegendary=json['is_legendary'])
