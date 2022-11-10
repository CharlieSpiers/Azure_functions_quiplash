"""
This file should be used to make sure that all pulls from and pushes to the databases are in the correct format
Resources used: https://pypi.org/project/schema/
"""
from schema import Schema, And, SchemaError


def _validate(dict_to_validate, schema):
    """
    :param dict_to_validate: Player or Prompt dict
    :param schema: Corresponding schema
    :return: The validated dict
    :except: incorrect_format_exception
    """
    try:
        return schema.validate(dict_to_validate)
    except SchemaError:
        raise incorrect_format_exception


def validate_player_dict(player):
    """
    :param player: Dict to validate
    :return: The validated dict
    :except: incorrect_format_exception
    """
    player_schema = Schema({
        'username': And(str, lambda n: 4 <= len(n) <= 16),
        'password': And(str, lambda n: 8 <= len(n) <= 24),
        'games_played': int,
        'total_score': int
    })
    return _validate(player, player_schema)


def convert_prompt_dict(prompt):
    """
    :param prompt: Dict to validate
    :return: The validated dict
    :except: incorrect_format_exception
    """
    prompt_schema = Schema({
        'id': int,
        'username': And(str, lambda n: 4 <= len(n) <= 16),
        'text': str
    })
    return _validate(prompt, prompt_schema)


class incorrect_format_exception(Exception):
    pass
