import json

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
    user_json = {
        'username': username,
        'password': password,
        'games_played': 0,
        'total_score': 0
    }

    try:
        player_container.create_item(body=user_json)
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
        return player_container.read_item(username)
    except exceptions.CosmosHttpResponseError:
        print("Username was not found")
        raise not_a_player_exception


def update_player(user_json):
    verify_player(user_json['username'], user_json['password'])

    player_container = _get_player_container()
    # TODO: Update the player in the database


def get_all_players():
    player_container = _get_player_container()
    return player_container.read_all_items()


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
