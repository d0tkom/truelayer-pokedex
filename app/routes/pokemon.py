from fastapi import APIRouter

from app.models import Pokemon, Dialect
from app.services.funtranslations import translate_text
from app.services.pokeapi import get_pokemon

router = APIRouter()


@router.get("/{name}", response_model=Pokemon, summary="Returns basic info about the requested pokemon species")
async def pokemon(name: str) -> Pokemon:
    """
    Returns basic info about the requested pokemon species:

    - **name**: the name of the pokemon species
    - **description**: a brief description of the pokemon
    - **habitat**: the habitat this pokemon species can be encountered in
    - **isLegendary**: whether or not this is a legendary pokemon
    """
    return get_pokemon(name)


@router.get("/translated/{name}", response_model=Pokemon, summary="Returns basic info about the requested pokemon "
                                                                  "species, with a fun description")
async def pokemon_translated(name: str) -> Pokemon:
    """
    Returns basic info about the requested pokemon species, with a fun description:

    - **name**: the name of the pokemon species
    - **description**: a brief description of the pokemon, with a fun dialect
    - **habitat**: the habitat this pokemon species can be encountered in
    - **isLegendary**: whether or not this is a legendary pokemon
    """
    poke = get_pokemon(name)

    dialect = Dialect.YODA if poke.habitat == 'cave' or poke.isLegendary else Dialect.SHAKESPEARE
    translated_description = translate_text(poke.description, dialect)

    return Pokemon(name=poke.name,
                   description=translated_description,
                   habitat=poke.habitat,
                   isLegendary=poke.isLegendary)
