"""Unit tests for bring-api."""

import aiohttp
from aioresponses import aioresponses
from dotenv import load_dotenv
import pytest

from bring_api.bring import Bring

load_dotenv()
UUID = "00000000-00000000-00000000-00000000"

BRING_LOGIN_RESPONSE = {
    "uuid": UUID,
    "publicUuid": UUID,
    "email": "EMAIL",
    "name": "NAME",
    "photoPath": "",
    "bringListUUID": UUID,
    "access_token": "ACCESS_TOKEN",
    "refresh_token": "REFRESH_TOKEN",
    "token_type": "Bearer",
    "expires_in": 604799,
}

BRING_USER_ACCOUNT_RESPONSE = {"userLocale": {"language": "de", "country": "DE"}}

BRING_USER_SETTINGS_RESPONSE = {
    "usersettings": [],
    "userlistsettings": [
        {
            "listUuid": UUID,
            "usersettings": [{"key": "listArticleLanguage", "value": "de-DE"}],
        }
    ],
}

BRING_LOAD_LISTS_RESPONSE = {
    "lists": [
        {
            "listUuid": UUID,
            "name": "Einkauf",
            "theme": "ch.publisheria.bring.theme.home",
        },
    ]
}

BRING_GET_LIST_RESPONSE = {
    "uuid": UUID,
    "status": "SHARED",
    "items": {
        "purchase": [
            {
                "uuid": "43bdd5a2-740a-4230-8b27-d0bbde886da7",
                "specification": "grün",
                "itemId": "Paprika",
            },
            {
                "uuid": "2de9d1c0-c211-4129-b6c5-c1260c3fc735",
                "specification": "gelb",
                "itemId": "Zucchetti",
            },
            {
                "uuid": "5681ed79-c8e4-4c8b-95ec-112999d016c0",
                "specification": "rot",
                "itemId": "Paprika",
            },
            {
                "uuid": "01eea2cd-f433-4263-ad08-3d71317c4298",
                "specification": "",
                "itemId": "Pouletbrüstli",
            },
        ],
        "recently": [],
    },
}

BRING_GET_ALL_ITEM_DETAILS_RESPONSE = [
    {
        "uuid": "bfb5634c-d219-4d66-b68e-1388e54f0bb0",
        "itemId": "Milchreis",
        "listUuid": UUID,
        "userIconItemId": "Reis",
        "userSectionId": "Getreideprodukte",
        "assignedTo": "",
        "imageUrl": "",
    },
    {
        "uuid": "0056b23c-7fc3-44da-8c34-426f8b632220",
        "itemId": "Zitronensaft",
        "listUuid": UUID,
        "userIconItemId": "Zitrone",
        "userSectionId": "Zutaten & Gewürze",
        "assignedTo": "",
        "imageUrl": "",
    },
]


@pytest.fixture(name="session")
async def aiohttp_client_session():
    """Create  a client session."""
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture(name="bring")
async def bring_api_client(session):
    """Create Bring instance."""
    bring = Bring(session, "EMAIL", "PASSWORD")
    return bring


@pytest.fixture(name="mocked")
def aioclient_mock():
    """Mock Aiohttp client requests."""
    with aioresponses() as m:
        yield m
