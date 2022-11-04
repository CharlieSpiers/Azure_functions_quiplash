import logging
import json
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import config as config

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    player_name = req.get_json().get('username')
    player_password = req.get_json().get('password')

    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'])
    db_client = client.get_database_client(config.settings['db_id'])

    if not (4 < len(player_name) < 16):
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Username less than 4 characters or more than 16 characters"})
        )
    elif not (8 < len(player_password) < 24):
        return func.HttpResponse(
            body=json.dumps({"result": False, "msg": "Password less than 8 characters or more than 24 characters"})
        )
