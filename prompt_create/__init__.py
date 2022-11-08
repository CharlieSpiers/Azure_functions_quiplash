import logging
import json

import azure.functions as func
from player_database_functions import verify_player, not_a_player_exception, incorrect_password_exception
from prompt_database_functions import add_prompt, prompt_already_exists_exception, check_players_prompts


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Create: parsing request')

    player_name = req.get_json().get("username")
    player_password = req.get_json().get("password")
    prompt_text = req.get_json().get("text")

    if not (20 <= len(prompt_text) <= 100):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "prompt length is <20 or > 100 characters"}))

    try:
        verify_player(player_name, player_password)
        check_players_prompts(player_name, prompt_text)
        add_prompt(player_name, prompt_text)
        return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))

    except (not_a_player_exception, incorrect_password_exception):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "bad username or password"}))

    except prompt_already_exists_exception:
        bad_prompt_message = "This user already has a prompt with the same text"
        return func.HttpResponse(body=json.dumps({"result": False, "msg": bad_prompt_message}))
