import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import controller.initialization
import settings

__author__ = 'Benoit Vander Stappen'


def init_db():
    if settings.db.cred_file:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.db.cred_file
    # cloud environment
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': settings.db.project_id,
    })
    return firestore.client()


def backend(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return '', 204, headers

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    settings.parse()
    db = init_db()
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'target' in request_json:
            if request_json['target'] == "new_schedule":
                try:
                    controller.initialization.create_new_db(
                        db,
                        request_json["nb_games"],
                        request_json["categories"],
                    )
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    return "Something wrong happened", 500, headers
                return "DB successfully initialized", 200, headers
        else:
            print("JSON is invalid, or missing a 'name' property")
            raise ValueError("JSON is invalid, or missing a 'name' property")
    else:
        print("Unknown content type: {}".format(content_type))
        raise ValueError("Unknown content type: {}".format(content_type))
