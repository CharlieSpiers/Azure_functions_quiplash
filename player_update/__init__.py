import logging
import json
import traceback

import azure.functions as func

from database_functions import verify_player, not_a_player_exception, incorrect_password_exception, update_player


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    add_to_score = get_integer_property(req.get_json(), "add_to_score")
    add_to_games_played = get_integer_property(req.get_json(), "add_to_games_played")

    # Do they want us to check if both values are 0? The rest of this is pointless if it is

    if add_to_games_played < 0 or add_to_score < 0:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Value to add is <=0"}))

    try:
        user = verify_player(player_name, player_password)

    except not_a_player_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "json_data does not exist"}))

    except incorrect_password_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "wrong password"}))

    # noinspection PyBroadException
    try:
        user['total_score'] = user['total_score'] + add_to_score
        user['games_played'] = user['games_played'] + add_to_games_played
        update_player(user)
    except Exception:
        print("Something unexpected went wrong")
        logging.error(traceback.format_exc())
        return func.HttpResponse(status_code=500)

    return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))


def get_integer_property(json_data, property_name):
    try:
        return int(json_data.get(property_name))
    except ValueError:
        return 0
