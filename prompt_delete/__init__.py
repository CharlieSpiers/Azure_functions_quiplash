import json
import logging

import azure.functions as func
from shared_code.player_database_functions import incorrect_password_exception, not_a_player_exception
from shared_code.prompt_database_functions import verify_player_and_prompt, not_a_prompt_exception, delete_prompt_by_id, access_denied_exception


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Delete: parsing request')

    try:
        prompt_id = int(req.get_json().get("id"))
        player_name = req.get_json().get("username")
        player_password = req.get_json().get("password")

        logging.info('Delete: verifying player credentials and fetching prompt')
        verify_player_and_prompt(player_name, player_password, prompt_id)

        logging.info('Delete: deleting prompt')
        delete_prompt_by_id(prompt_id)
        return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))

    except (incorrect_password_exception, not_a_player_exception):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "bad username or password"}))

    except not_a_prompt_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "prompt id does not exist"}))

    except access_denied_exception:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "access denied"}))

    except (ValueError, Exception):
        logging.info("Malformed request")
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Malformed request"}))
