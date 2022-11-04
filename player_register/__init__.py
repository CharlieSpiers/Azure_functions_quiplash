import logging
import json

import azure.functions as func

import database_functions


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    if not (4 < len(player_name) < 16):
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Username less than 4 characters or more than 16 characters"})
        )
    elif not (8 < len(player_password) < 24):
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Password less than 8 characters or more than 24 characters"})
        )

    # if the credentials are the correct length, try to add to the database:
    try:
        database_functions.add_player(player_name, player_password)
        return func.HttpResponse(
            body=json.dumps({"result": True, "msg": "OK"})
        )

    except database_functions.user_already_exists_exception:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Username already exists"})
        )
