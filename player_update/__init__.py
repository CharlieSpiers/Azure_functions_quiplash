import logging
import json
import traceback

import azure.functions as func

import database_functions


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    add_to_score = get_property(req.get_json(), "add_to_score")
    add_to_games_played = get_property(req.get_json(), "add_to_games_played")

    # Do they want us to check if both values are 0? The rest of this is pointless if it is

    if add_to_games_played < 0 or add_to_score < 0:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Value to add is <=0"})
        )

    try:
        user = database_functions.verify_player(player_name, player_password)

    except database_functions.not_a_user_exception:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "user does not exist"})
        )

    except database_functions.incorrect_password_exception:
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "wrong password"})
        )

    # noinspection PyBroadException
    try:
        user['add_to_score'] = user['add_to_score'] + add_to_score
        user['add_to_games_played'] = user['add_to_games_played'] + add_to_games_played
        database_functions.update_player(user)
    except Exception:
        print("Something unexpected went wrong")
        logging.error(traceback.format_exc())
        return func.HttpResponse(status_code=500)

    return func.HttpResponse(
        body=json.dumps({"result": True, "msg": "OK"})
    )


def get_property(user, property_name):
    try:
        return int(user.get(property_name))
    except ValueError:
        return 0
