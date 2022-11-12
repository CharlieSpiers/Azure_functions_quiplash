import json
import logging

import azure.functions as func
from shared_code.prompt_database_functions import query_prompts


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get_text: parsing request')

    try:
        word = req.get_json().get("word")
        exact = bool(req.get_json().get("exact"))

        if exact:
            regex = f"([[:<:]]){word}([[:>:]])"
        else:
            regex = f"([[:<:]])(?i){word}([[:>:]])"

        logging.info('Get_text: sending query')
        query = f"SELECT prompt.text, prompt.username, prompt.id FROM prompt WHERE " \
                f"RegexMatch(prompt.text, '{regex}')"

        return func.HttpResponse(body=json.dumps(list(query_prompts(query))))

    except (TypeError, ValueError):
        logging.info('Get_text: something went wrong')
        return func.HttpResponse(status_code=500)
