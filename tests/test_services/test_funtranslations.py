import json
from http import HTTPStatus
from unittest import TestCase, mock
from unittest.mock import patch

import requests

from app.models import Dialect, Pokemon
from app.services.funtranslations import translate_text

RESOURCES = './resources'

FUNTRANSLATIONS_MEWTWO_SHAKESPEARE_JSON = f'{RESOURCES}/funtranslations-translate-shakespeare.json'
FUNTRANSLATIONS_MEWTWO_YODA_JSON = f'{RESOURCES}/funtranslations-translate-yoda.json'

MEWTWO: Pokemon = Pokemon(description='It was created by a scientist after years of horrific gene splicing and DNA '
                                      'engineering experiments.', habitat='rare', isLegendary=True, name='mewtwo')
MEWTWO_SHAKESPEARE_DESCRIPTION = "'t wast did create by a scientist after years of horrific gene splicing and dna engineering experiments."
MEWTWO_YODA_DESCRIPTION = 'Created by a scientist after years of horrific gene splicing and dna engineering experiments, it was.'


class Test(TestCase):
    @staticmethod
    def _mock_response(data_file):
        resp = mock.Mock()
        resp.status_code = HTTPStatus.OK

        with open(data_file) as f:
            mock_api_response_data = f.read()
            resp.json.return_value = json.loads(mock_api_response_data)

        return resp

    @patch('app.services.funtranslations.requests.post')
    def test_translate_text_to_shakespeare(self, mock_post):
        mock_post.return_value = self._mock_response(FUNTRANSLATIONS_MEWTWO_SHAKESPEARE_JSON)

        expected = MEWTWO_SHAKESPEARE_DESCRIPTION
        actual = translate_text(MEWTWO.description, Dialect.SHAKESPEARE)

        mock_post.return_value.raise_for_status.assert_called_once()
        self.assertEqual(expected, actual)

    @patch('app.services.funtranslations.requests.post')
    def test_translate_text_to_yoda(self, mock_post):
        mock_post.return_value = self._mock_response(FUNTRANSLATIONS_MEWTWO_YODA_JSON)

        expected = MEWTWO_YODA_DESCRIPTION
        actual = translate_text(MEWTWO.description, Dialect.YODA)

        mock_post.return_value.raise_for_status.assert_called_once()
        self.assertEqual(expected, actual)

    @patch('app.services.funtranslations.requests.post')
    def test_translate_text_returns_same_text_if_http_error(self, mock_post):
        mock_resp = requests.models.Response()
        mock_resp.status_code = HTTPStatus.TOO_MANY_REQUESTS
        mock_post.return_value = mock_resp

        expected = MEWTWO.description
        actual = translate_text(MEWTWO.description, Dialect.YODA)

        self.assertEqual(expected, actual)

    @patch('app.services.funtranslations.logger.exception')
    @patch('app.services.funtranslations.requests.post')
    def test_translate_text_returns_same_text_and_logs_if_http_erro_but_not_429(self, mock_post, mock_logger):
        mock_resp = requests.models.Response()
        mock_resp.status_code = HTTPStatus.UNAUTHORIZED  # just pick another error code randomly
        mock_post.return_value = mock_resp

        expected = MEWTWO.description
        actual = translate_text(MEWTWO.description, Dialect.YODA)

        mock_logger.assert_called_once()
        self.assertEqual(expected, actual)
