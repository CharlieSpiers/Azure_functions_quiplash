import random

from azure import cosmos
import azure.cosmos.exceptions as exceptions
import config

from shared_code.player_database_functions import verify_player


def add_prompt(username, text):
    """
    Adds a new prompt if it does not already exist
    Throws prompt_already_exists_exception
    """
    prompt_container = _get_prompt_container()

    # Nice big random integer
    random_id = int((random.random() * (10**10)) * random.random() * (10**10))
    prompt_dict = {
        'id': str(random_id),
        'username': username,
        'text': text
    }
    try:
        prompt_container.create_item(prompt_dict)
    except exceptions.CosmosHttpResponseError as e:
        print(e.message)


def verify_player_and_prompt(username, password, prompt_id):
    verify_player(username, password)
    prompt = get_prompt_by_id(prompt_id)
    if prompt['username'] != username:
        raise access_denied_exception
    else:
        return prompt


def update_prompt(prompt):
    prompt_container = _get_prompt_container()
    prompt_container.upsert_item(prompt)


def query_prompts(query):
    prompt_container = _get_prompt_container()
    return prompt_container.query_items(query=query)


def get_players_prompts(username):
    return query_prompts(f'SELECT * FROM prompt p WHERE p.username = "{username}"')


def get_all_prompts():
    prompt_container = _get_prompt_container()
    return prompt_container.read_all_items()


def check_players_prompts(username, new_prompt_text):
    for prompt in get_players_prompts(username):
        if prompt['text'] == new_prompt_text:
            return prompt_already_exists_exception


def get_prompt_by_id(prompt_id):
    prompt_container = _get_prompt_container()
    try:
        return prompt_container.read_item(item=str(prompt_id), partition_key=str(prompt_id))

    except exceptions.CosmosHttpResponseError:
        raise not_a_prompt_exception


def delete_prompt_by_id(prompt_id):
    prompt_container = _get_prompt_container()
    prompt_container.delete_item(item=prompt_id, partition_key=prompt_id)


def _get_prompt_container():
    client = cosmos.cosmos_client.CosmosClient(config.settings['db_URI'], config.settings['db_key'])
    db_client = client.get_database_client(config.settings['db_id'])
    return db_client.get_container_client(config.settings['prompt_container'])


class prompt_already_exists_exception(Exception):
    pass


class not_a_prompt_exception(Exception):
    pass


class access_denied_exception(Exception):
    pass
