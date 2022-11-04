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

    except database_functions.not_a_user_exception:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "user does not exist"})
        )

    except database_functions.incorrect_password_exception:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "wrong password"})
        )

    # Now the user is verified:
    add_to_games_played = 0
    add_to_score = 0

    # TODO: Update the values there in try clauses

    if add_to_games_played < 0 or add_to_score < 0:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Value to add is <=0"})
        )

    # TODO: Add the values to the database

    return func.HttpResponse(
        body=json.dumps({"result": True, "msg": "OK"})
    )
