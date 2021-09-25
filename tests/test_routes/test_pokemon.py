from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException

from app.config import POKEMON_NOT_FOUND, EXTERNAL_API_FAILED
from app.main import app
from app.models import Pokemon, Dialect

POKEMON: Pokemon = Pokemon(name='name', description='description', habitat='habitat', isLegendary=False)
LEGENDARY_POKEMON: Pokemon = Pokemon(name='name', description='legendary_description', habitat='habitat',
                                     isLegendary=True)
CAVE_POKEMON: Pokemon = Pokemon(name='name', description='cave_description', habitat='cave', isLegendary=False)
CAVE_AND_LEGENDARY_POKEMON: Pokemon = Pokemon(name='name', description='cave_and_legendary_description', habitat='cave',
                                              isLegendary=True)
SHAKESPEARE_DESCRIPTION = 'shakespeare_description'
YODA_DESCRIPTION = 'yoda_description'


class Test(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_general_case(self, mock_get_pokemon):
        mock_get_pokemon.return_value = POKEMON

        response = self.client.get('/pokemon/name')

        expected = POKEMON
        actual = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_if_pokemon_not_found_returns_404(self, mock_get_pokemon):
        mock_get_pokemon.side_effect = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=POKEMON_NOT_FOUND)

        response = self.client.get('/pokemon/name')

        expected = {'detail': POKEMON_NOT_FOUND}
        actual = response.json()

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(expected, actual)

    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_if_api_down_returns_503(self, mock_get_pokemon):
        mock_get_pokemon.side_effect = HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                                                     detail=EXTERNAL_API_FAILED)

        response = self.client.get('/pokemon/name')

        expected = {'detail': EXTERNAL_API_FAILED}
        actual = response.json()

        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE, response.status_code)
        self.assertEqual(expected, actual)

    @patch('app.routes.pokemon.translate_text')
    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_translated_returns_back_pokemon_with_translated_description(self, mock_get_pokemon,
                                                                                 mock_translate_text):
        mock_get_pokemon.return_value = POKEMON
        mock_translate_text.return_value = SHAKESPEARE_DESCRIPTION

        response = self.client.get('/pokemon/translated/name')

        expected = Pokemon(name=POKEMON.name,
                           description=SHAKESPEARE_DESCRIPTION,
                           habitat=POKEMON.habitat,
                           isLegendary=POKEMON.isLegendary)
        actual = response.json()

        mock_translate_text.assert_called_with(POKEMON.description, Dialect.SHAKESPEARE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, actual)

    @patch('app.routes.pokemon.translate_text')
    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_translated_normal_pokemon_requests_shakespeare_translation(self, mock_get_pokemon: Mock,
                                                                                mock_translate_text: Mock):
        mock_get_pokemon.return_value = POKEMON
        mock_translate_text.return_value = 'translated_text'

        response = self.client.get('/pokemon/translated/name')

        mock_translate_text.assert_called_with(POKEMON.description, Dialect.SHAKESPEARE)
        self.assertEqual(200, response.status_code)

    @patch('app.routes.pokemon.translate_text')
    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_translated_legendary_pokemon_requests_yoda_translation(self, mock_get_pokemon,
                                                                            mock_translate_text):
        mock_get_pokemon.return_value = LEGENDARY_POKEMON
        mock_translate_text.return_value = 'translated_text'

        response = self.client.get('/pokemon/translated/name')

        mock_translate_text.assert_called_with(LEGENDARY_POKEMON.description, Dialect.YODA)
        self.assertEqual(200, response.status_code)

    @patch('app.routes.pokemon.translate_text')
    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_translated_cave_pokemon_requests_yoda_translation(self, mock_get_pokemon, mock_translate_text):
        mock_get_pokemon.return_value = CAVE_POKEMON
        mock_translate_text.return_value = 'translated_text'

        response = self.client.get('/pokemon/translated/name')

        mock_translate_text.assert_called_with(CAVE_POKEMON.description, Dialect.YODA)
        self.assertEqual(200, response.status_code)

    @patch('app.routes.pokemon.translate_text')
    @patch('app.routes.pokemon.get_pokemon')
    def test_pokemon_translated_cave_and_legendary_pokemon_requests_yoda_translation(self, mock_get_pokemon,
                                                                                     mock_translate_text):
        mock_get_pokemon.return_value = CAVE_AND_LEGENDARY_POKEMON
        mock_translate_text.return_value = 'translated_text'

        response = self.client.get('/pokemon/translated/name')

        mock_translate_text.assert_called_with(CAVE_AND_LEGENDARY_POKEMON.description, Dialect.YODA)
        self.assertEqual(200, response.status_code)
