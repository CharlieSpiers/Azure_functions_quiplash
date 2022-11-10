import json
import logging

import azure.functions as func

from shared_code.player_database_functions import query_players


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Leaderboard: parsing request")
    top_k = int(req.get_json().get('top'))
    if not top_k > 0:
        return func.HttpResponse(body=json.dumps([]))

    logging.info("Leaderboard: sending query to database")
    sql_query = f'SELECT TOP {top_k} * FROM player p ORDER BY p.total_score DESC, p.username ASC'

    logging.info("Leaderboard: returning leaderboard")
    return_players = []
    for player in query_players(sql_query):
        return_players.append({
            "username": player["username"],
            "score": player["total_score"],
            "games_played": player["games_played"]
        })
    return func.HttpResponse(body=json.dumps(return_players))
