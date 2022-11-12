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
    sql_query = f'SELECT TOP {top_k} p.username, p.total_score as score, p.games_played FROM player p ORDER BY p.total_score DESC, p.username ASC'
    return func.HttpResponse(body=json.dumps(list(query_players(sql_query))))
