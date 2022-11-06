import json
import logging

import azure.functions as func

from database_functions import get_all_players


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    top_k = int(req.get_json().get('top'))
    if not top_k > 0:
        return func.HttpResponse(body=json.dumps([]))

    players = get_all_players()
    sorted_by_name = sorted(players, key=lambda x: x['username'])
    sorted_by_score = sorted(sorted_by_name, key=lambda x: x['total_score'])

    return func.HttpResponse(body=json.dumps(sorted_by_score[:top_k]))
