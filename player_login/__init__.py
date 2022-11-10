import logging
import json

import azure.functions as func
from shared_code.player_database_functions import verify_player, not_a_player_exception, incorrect_password_exception


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Login: parsing request')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    try:
        logging.info('Login: verifying player')
        verify_player(player_name, player_password)
    except (not_a_player_exception, incorrect_password_exception):
        logging.info('Login: incorrect credentials')
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username or password incorrect"}))

    logging.info('Login: correct credentials')
    return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))

