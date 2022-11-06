import logging
import json

import azure.functions as func
from database_functions import verify_player, not_a_player_exception, incorrect_password_exception


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    try:
        verify_player(player_name, player_password)
    except (not_a_player_exception, incorrect_password_exception):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username or password incorrect"}))

    return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))

