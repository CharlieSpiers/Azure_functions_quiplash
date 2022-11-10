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
    return func.HttpResponse(body=json.dumps(query_players(sql_query)))

    # logging.info("Leaderboard: requesting all players")
    # players = get_all_players()
    #
    # logging.info("Leaderboard: sorting players")
    # sorted_by_name = sorted(players, key=lambda x: x['username'])
    # sorted_by_score = sorted(sorted_by_name, key=lambda x: x['total_score'])
    #
    # logging.info("Leaderboard: returning leaderboard")
    # return func.HttpResponse(body=json.dumps(sorted_by_score[:top_k]))
