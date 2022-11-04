import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    matches_database = True  # TODO

    if matches_database:
        return func.HttpResponse(
            body=json.dumps({"result": True, "msg": "OK"})
        )
    else:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Username or password incorrect"})
        )
