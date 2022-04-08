# Backend

## Use

### Architecture

The backend is made of one single function called `backend`. However, several actions can be performed by the backend. The action is defined through the `target` parameter.

### Targets

Atm, there is only one target: `new_schedule`

#### New schedule

Clear the collections `games` `matches` & `teams` and create a new schedule. The content of the request must be as follows:

| Key      | Value                                                 |
| -------- | ----------------------------------------------------- |
| target   | `new_schedule`                                        |
| nb_games | int: amount of games **per circuit**                  |
| csv_path | str: path to the csv file with the configuration data |

The script creates games, matches & teams. It shuffles teams across every circuits but it ensures a team only plays in a single circuit. 

Players from one category never play with players from another section (called categories in the python conde. For instance,  `Louveteaux` always plays against `Louveteaux`.

Circuits are defined in the order of the category definitions.

Data is loaded from the file located in `csv_path`. This file must observe these rules:

- First row contains the headers (i.e. the name/key of every value)
- The next rows define the sections, one row/section
- The header values must match the value of the `csv.headers` settings in the `settings.yml` file
- The headers listed in the `settings.yml` file are required in the csv file

The delimiter of the csv file can be defined is the `settings.yml` file.

See tests below for more details.

## Setup

1. Create a service account & generate a private key file for it [as explained here](https://firebase.google.com/docs/admin/setup#initialize-sdk).
2. Parse your Firebase credentials in a `backend/cred.json` file
3. Parse the Firebase project ID in `settings.yml`

## Deploy

### Requirements

- [gcloud CLI](https://cloud.google.com/sdk/install?hl=fr)

### Steps

````sh
gclound init
gcloud functions deploy backend --runtime python37 --trigger-http --region europe-west1
````

## Test

### Warning

Performing this test will **wipe the database**

### With pytest

````sh
export TRIGGER_URL=https://europe-west1-badenbattle-a0dec.cloudfunctions.net/backend 
pytest test\test_db_init.py
````

### With GCP console

***This section is obsolete***

1. Go to the [testing tab of the function](https://console.cloud.google.com/functions/details/europe-west1/backend?project=badenbattle-a0dec&tab=testing)
2. Paste the following json request

````json
{
    "target": "new_schedule",
    "nb_games": 5,
    "nb_circuit": 2,
    "categories": {
        "loups": [
            {"name": "Ferao", "teams": 6},
            {"name": "Waig", "teams": 2},
            {"name": "Braine", "teams": 2}
        ],
        "lutins": [
            {"name": "Ecureil", "teams": 5},
            {"name": "Feux-follets", "teams": 5}
        ]
    }
}
````

