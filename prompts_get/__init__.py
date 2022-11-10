import json
import logging
import random

import azure.functions as func

from shared_code.prompt_database_functions import get_all_prompts, get_players_prompts


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get_prompt: parsing request')

    try:
        prompt_number = int(req.get_json().get("prompts"))
        prompts = list(get_all_prompts())
        return func.HttpResponse(body=json.dumps(prompts[:prompt_number]))
    except (TypeError, ValueError):
        logging.info("Get_prompt: there was no prompt_number, trying players")
        players = req.get_json().get("players")
        prompts = []
        for player in players:
            prompts.extend(get_players_prompts(player))
        return func.HttpResponse(body=json.dumps(prompts))
