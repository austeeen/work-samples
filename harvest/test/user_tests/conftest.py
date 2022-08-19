"""
conftest.py
"""

import os
import json
import pytest
import responses


def load(json_path):
    return json.load(open(json_path, 'r'))


@pytest.fixture(scope='session', autouse=True)
def set_home():
    # PRIVATE


"""
config_fixtures.py
"""


@pytest.fixture
def conf_base_url():
    return # PRIVATE


@pytest.fixture
def conf_data_path():
    return # PRIVATE


@pytest.fixture
def conf_bot_name():
    return # PRIVATE


@pytest.fixture
def conf_bot_id():
    return # PRIVATE


@pytest.fixture
def conf_scan_id():
    return # PRIVATE


@pytest.fixture
def conf_play_id():
    return # PRIVATE


@pytest.fixture
def conf_command_id():
    return # PRIVATE


@pytest.fixture
def conf_on():
    return # PRIVATE


@pytest.fixture
def conf_within():
    return # PRIVATE


@pytest.fixture
def conf_since():
    return # PRIVATE


@pytest.fixture
def conf_past():
    return # PRIVATE


"""
response_fixtures.py
"""


@pytest.fixture
def resp_get_from_id(PRIVATE_PARAMS):
    return responses.Response(PRIVATE,
        status=200)


@pytest.fixture
def resp_get_from_name(PRIVATE_PARAMS):
    return responses.Response(PRIVATE,
        status=200)


@pytest.fixture
def resp_get_play_id(PRIVATE_PARAMS):
    return responses.Response(PRIVATE,
        status=200)


@pytest.fixture
def resp_get_bot_id_from_play_id(PRIVATE_PARAMS):
    return responses.Response(PRIVATE,
        status=200)


@pytest.fixture
def resp_cancel_command(PRIVATE_PARAMS):
    return responses.Response(PRIVATE,
        status=200)
