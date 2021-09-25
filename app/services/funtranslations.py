import logging
from http import HTTPStatus

import requests
from requests import HTTPError

from app.config import FUNTRANSLATIONS_TRANSLATE_URL
from app.models import Dialect

logger = logging.getLogger('gunicorn.error')


def translate_text(text: str, dialect: Dialect) -> str:
    try:
        response = requests.post(f'{FUNTRANSLATIONS_TRANSLATE_URL}/{dialect.name}', data={'text': text})
        response.raise_for_status()
    except HTTPError as e:
        if e.response.status_code != HTTPStatus.TOO_MANY_REQUESTS:
            logger.exception(e)  # log this exception, as we failed for an unexpected reason
        return text

    json = response.json()

    return json['contents']['translated']
