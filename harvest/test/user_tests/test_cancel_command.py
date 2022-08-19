"""
test_list_plays.py
"""

import responses

from tools.cancel_command import main


@responses.activate
def test_cancel_command(PRIVATE_PARAMS):
    # PRIVATE
