# project configs

VERSION = "0.0.0"
PROJECT_NAME: str = 'Pokedex'

# external api configs

POKEAPI_BASE_URL = 'https://pokeapi.co/api/v2'
FUNTRANSLATIONS_BASE_URL = 'https://api.funtranslations.com'

POKEAPI_SPECIES_URL = f'{POKEAPI_BASE_URL}/pokemon-species'
FUNTRANSLATIONS_TRANSLATE_URL = f'{FUNTRANSLATIONS_BASE_URL}/translate'

# API messages

EXTERNAL_API_FAILED = 'Service unavailable'
POKEMON_NOT_FOUND = 'Item not found'