from typing import Iterable, Any

from azure import cosmos
import azure.cosmos.exceptions as exceptions
import config


def verify_player(username, password):
    """
    Uses get_player, then checks their password matches.
    Throws incorrect_password_exception and inherited exceptions
    Returns the json_data in json_data if password matches
    """
    user = get_player(username)
    if user['password'] != password:
        print("password was incorrect")
        raise incorrect_password_exception
    else:
        return user


def add_player(username, password):
    """
    Adds a new json_data if they do not already exist
    Throws player_already_exists_exception
    """
    player_container = _get_player_container()
    player_dict = {
        'username': username,
        'password': password,
        'games_played': 0,
        'total_score': 0
    }
    try:
        player_container.create_item(player_dict)
    except exceptions.CosmosHttpResponseError:
        raise player_already_exists_exception


def get_player(username):
    """
    Gets the json_data object, if it exists
    Throws not_a_player_exception
    Returns the json_data in json_data if they exists
    """
    player_container = _get_player_container()
    try:
        return player_container.read_item(item=username, partition_key=username)

    except exceptions.CosmosHttpResponseError:
        raise not_a_player_exception


def update_player(player_dict, verify=True):
    if verify:
        verify_player(player_dict['username'], player_dict['password'])

    player_container = _get_player_container()
    player_container.upsert_item(player_dict)


def query_players(query: str) -> Iterable[dict[str, Any]]:
    player_container = _get_player_container()
    return player_container.query_items(query=query, enable_cross_partition_query=True)


def _get_player_container():
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'])
    db_client = client.get_database_client(config.settings['db_id'])
    return db_client.get_container_client(config.settings['player_container'])


class not_a_player_exception(Exception):
    pass


class incorrect_password_exception(Exception):
    pass


class player_already_exists_exception(Exception):
    pass
