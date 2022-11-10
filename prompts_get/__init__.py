import json
import logging
import random

import azure.functions as func

from shared_code.prompt_database_functions import get_all_prompts


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get_prompt: parsing request')

    # try:
    prompt_number = int(req.get_json().get("prompts"))

    prompts = get_all_prompts()
    random.shuffle(prompts)
    return func.HttpResponse(body=json.dumps(prompts[:prompt_number]))

    # except Exception:
    #     print("aaa")
