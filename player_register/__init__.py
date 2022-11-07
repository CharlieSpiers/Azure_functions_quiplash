import logging
import json

import azure.functions as func

from player_database_functions import add_player, player_already_exists_exception


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get("username")
    player_password = req.get_json().get("password")

    if not (4 <= len(player_name) <= 16):
        bad_username_message = "Username less than 4 characters or more than 16 characters"
        return func.HttpResponse(body=json.dumps({"result": False, "msg": bad_username_message}))

    elif not (8 <= len(player_password) <= 24):
        bad_password_message = "Password less than 8 characters or more than 24 characters"
        return func.HttpResponse(body=json.dumps({"result": False, "msg": bad_password_message}))

    # if the credentials are the correct length, try to add to the database:
    try:
        add_player(player_name, player_password)
        return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))

    except player_already_exists_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username already exists"}))
