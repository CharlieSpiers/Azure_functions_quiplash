"""
This file should be used to make sure that all pulls from and pushes to the databases are in the correct format
Resources used: https://pypi.org/project/schema/
"""
from schema import Schema, And, SchemaError
import json


def _validate(dict_to_validate, schema):
    """
    :param dict_to_validate: Player or Prompt dict
    :param schema: Corresponding schema
    :return: The (validated) dict converted to json - may be different to the input
    :except: incorrect_format_exception
    """
    try:
        validated = schema.validate(dict_to_validate)
        return json.dumps(validated)
    except SchemaError:
        raise incorrect_format_exception


def validate_player_dict(player, return_as_json=False):
    """
    :param return_as_json: Return the validated dict in validated_json format
    :param player: Dict to validate
    :return: The dict in validated_json.dumps() format
    :except: incorrect_format_exception
    """
    player_schema = Schema({
        'username': And(str, lambda n: 4 <= len(n) <= 16),
        'password': And(str, lambda n: 8 <= len(n) <= 24),
        'games_played': int,
        'total_score': int
    })
    validated_json = _validate(player, player_schema)
    if return_as_json:
        return validated_json


def convert_prompt_dict(prompt, return_as_json=False):
    """
    :param return_as_json: Return the validated dict in validated_json format
    :param prompt: Dict to validate
    :return: The dict in json.dumps() format
    :except: incorrect_format_exception
    """
    prompt_schema = Schema({
        'id': int,
        'username': And(str, lambda n: 4 <= len(n) <= 16),
        'text': str
    })
    validated_json = _validate(prompt, prompt_schema)
    if return_as_json:
        return validated_json


class incorrect_format_exception(Exception):
    pass
