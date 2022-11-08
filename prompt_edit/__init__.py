import json
import logging

import azure.functions as func
from player_database_functions import incorrect_password_exception, not_a_player_exception
from prompt_database_functions import verify_player_and_prompt, update_prompt, check_players_prompts
from prompt_database_functions import not_a_prompt_exception, access_denied_exception, prompt_already_exists_exception


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Edit: parsing request')

    try:
        prompt_id = int(req.get_json().get("id"))
        player_name = req.get_json().get("username")
        player_password = req.get_json().get("password")
        new_text = req.get_json().get("text")

        if not (20 <= len(new_text) <= 100):
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "prompt length is <20 or > 100 characters"}))

        logging.info('Edit: checking if the user already has this prompt text')
        check_players_prompts(player_name, new_text)

        logging.info('Edit: verifying player credentials and fetching prompt')
        prompt = verify_player_and_prompt(player_name, player_password, prompt_id)

        logging.info('Edit: updating prompt')
        prompt['text'] = new_text
        update_prompt(prompt)
        return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))

    except (incorrect_password_exception, not_a_player_exception):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "bad username or password"}))

    except not_a_prompt_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "prompt id does not exist"}))

    except access_denied_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "access denied"}))

    except prompt_already_exists_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "This user already has a prompt with the same text"}))

    except ValueError:
        logging.info("Malformed request")
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Malformed request"}))
