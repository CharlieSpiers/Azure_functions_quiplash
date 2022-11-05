import logging
import json

import azure.functions as func
import database_functions


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    try:
        database_functions.verify_player(player_name, player_password)
    except database_functions.not_a_player_exception or database_functions.incorrect_password_exception:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Username or password incorrect"})
        )

    return func.HttpResponse(
        body=json.dumps({"result": True, "msg": "OK"})
    )

