import os
import subprocess

import requests

TRIGGER_URL = os.getenv("TRIGGER_URL", "https://europe-west1-badenbattle-a0dec.cloudfunctions.net/backend")

TEST_REQUEST = {
    "target": "new_schedule",
    "nb_games": 5,
    "nb_circuit": 2,
    "categories": {
        "loups": [
            {"name": "Ferao", "teams": 6},
            {"name": "Waig", "teams": 2},
            {"name": "Braine", "teams": 2},
        ],
        "lutins": [
            {"name": "Ecureil", "teams": 5},
            {"name": "Feux-follets", "teams": 5},
        ],
    }
}

###########################################################
#         THESE TESTS ARE CURRENTLY OBSOLETE              #
# They are based on the previous API (before using a csv) #
###########################################################


def test_no_args():
    assert TRIGGER_URL is not ""

    oauth_token = subprocess.getoutput("gcloud auth print-identity-token")
    res = requests.get(TRIGGER_URL, headers=dict(Authorization=f"bearer {oauth_token}"))
    assert res.status_code != 200


def test_args():
    assert TRIGGER_URL is not ""

    oauth_token = subprocess.getoutput("gcloud auth print-identity-token")
    res = requests.post(TRIGGER_URL, json=TEST_REQUEST, headers=dict(Authorization=f"bearer {oauth_token}"))
    assert res.status_code == 200
    assert res.text == "DB successfully initialized"
