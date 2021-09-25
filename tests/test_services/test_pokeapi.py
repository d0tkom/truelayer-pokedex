import json
from http import HTTPStatus
from unittest import TestCase, mock
from unittest.mock import patch

import requests
from fastapi import HTTPException

from app.config import POKEMON_NOT_FOUND
from app.models import Pokemon
from app.services.pokeapi import get_pokemon

RESOURCES = './resources'

POKEAPI_MEWTWO_JSON = f'{RESOURCES}/pokeapi-pokemon-species-mewtwo.json'

MEWTWO: Pokemon = Pokemon(description='It was created by a scientist after years of horrific gene splicing and DNA '
                                      'engineering experiments.', habitat='rare', isLegendary=True, name='mewtwo')


class Test(TestCase):
    @staticmethod
    def _mock_response(data_file):
        resp = mock.Mock()
        resp.status_code = HTTPStatus.OK

        with open(data_file) as f:
            mock_api_response_data = f.read()
            resp.json.return_value = json.loads(mock_api_response_data)

        return resp

    @patch('app.services.pokeapi.requests.get')
    def test_get_pokemon_general_case(self, mock_get):
        mock_get.return_value = self._mock_response(POKEAPI_MEWTWO_JSON)

        expected = MEWTWO
        actual = get_pokemon('mewtwo')

        mock_get.return_value.raise_for_status.assert_called_once()
        self.assertEqual(expected, actual)

    @patch('app.services.pokeapi.requests.get')
    def test_get_pokemon_when_pokemon_not_found_throws_404(self, mock_get):
        mock_resp = requests.models.Response()
        mock_resp.status_code = HTTPStatus.NOT_FOUND
        mock_get.return_value = mock_resp

        with self.assertRaises(HTTPException) as msg:
            get_pokemon('mewtwo')

        e = msg.exception

        self.assertEqual(HTTPStatus.NOT_FOUND, e.status_code)
        self.assertEqual(POKEMON_NOT_FOUND, e.detail)

    @patch('app.services.pokeapi.requests.get')
    def test_get_pokemon_when_api_call_fails_throws_503(self, mock_get):
        mock_resp = requests.models.Response()
        mock_resp.status_code = HTTPStatus.UNAUTHORIZED
        mock_get.return_value = mock_resp

        with self.assertRaises(HTTPException) as msg:
            get_pokemon('mewtwo')

        e = msg.exception

        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE, e.status_code)
        self.assertEqual('Service unavailable', e.detail)
