import logging
import json

import azure.functions as func
from player_database_functions import verify_player, not_a_player_exception, incorrect_password_exception


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get("username")
    player_password = req.get_json().get("password")
    prompt_text = req.get_json().get("text")

    if not (20 <= len(prompt_text) <= 100):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "prompt length is <20 or > 100 characters"}))

    try:
        verify_player(player_name, player_password)
    except (not_a_player_exception, incorrect_password_exception):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "bad username or password"}))

    # if the credentials are the correct length, try to add to the database:
    try:
        add_player(player_name, player_password)
        return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))

    except player_already_exists_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username already exists"}))
