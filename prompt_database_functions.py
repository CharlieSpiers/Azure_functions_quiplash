from azure import cosmos
import azure.cosmos.exceptions as exceptions
import config


def add_prompt(username, text):
    """
    Adds a new json_data if they do not already exist
    Throws prompt_already_exists_exception
    """
    prompt_container = _get_prompt_container()
    # hash(username + ": " + text) will deterministically return an integer
    prompt_dict = {
        'id': abs(hash(username + ": " + text)),
        'username': username,
        'text': text
    }
    try:
        # As hash is deterministic, will collide if it's a duplicate
        prompt_container.create_item(prompt_dict)
    except exceptions.CosmosHttpResponseError:
        raise prompt_already_exists_exception


def _get_prompt_container():
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'])
    db_client = client.get_database_client(config.settings['db_id'])
    return db_client.get_container_client(config.settings['prompt_container'])


class prompt_already_exists_exception(Exception):
    pass
