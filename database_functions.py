from azure import cosmos
import azure.cosmos.exceptions as exceptions
import config


def verify_player(username, password):
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'])
    db_client = client.get_database_client(config.settings['db_id'])
    player_container = db_client.get_container_client(config.settings['player_container'])

    try:
        user = player_container.read_item(username)
        if user['password'] != password:
            print("password was incorrect")
            raise incorrect_password_exception

    except exceptions.CosmosHttpResponseError:
        print("Username was not found")
        raise not_a_user_exception


class not_a_user_exception(Exception):
    pass


class incorrect_password_exception(Exception):
    pass
