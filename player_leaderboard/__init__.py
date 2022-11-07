import json
import logging

import azure.functions as func

from player_database_functions import get_all_players


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Leaderboard: parsing response")
    top_k = int(req.get_json().get('top'))
    if not top_k > 0:
        return func.HttpResponse(body=json.dumps([]))

    logging.info("Leaderboard: requesting all players")
    players = get_all_players()

    logging.info("Leaderboard: sorting players")
    sorted_by_name = sorted(players, key=lambda x: x['username'])
    sorted_by_score = sorted(sorted_by_name, key=lambda x: x['total_score'])

    logging.info("Leaderboard: returning leaderboard")
    return func.HttpResponse(body=json.dumps(sorted_by_score[:top_k]))
