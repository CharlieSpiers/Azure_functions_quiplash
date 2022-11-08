"""
Wrapper File - COMP3207 Coursework 1 Part 1

Purposes of this file

1) Facilitate marking. Through it, we can run the marking script both on a local development server
   (on the code you hand in) and on what you deploy on your Azure account.

2) Assess your knowledge of how to configure the route of Azure Functions.

3) Assess your knowledge of how to configure authorisation levels for your FunctionApp.

"""

# Note this requirement, in case you run this from outside the venv you are working on
import requests
import config

# Set the 'function' authorization level on your deployment
# Put the relevant App key here (Refer to Lecture Thursday Week 4)
import player_database_functions

APP_KEY = config.settings['app_key']

LOCAL_SERVER = "http://localhost:7071/api"
# Replace below as appropriate
CLOUD_SERVER = config.settings['cloud_URI']


def player_register(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER

    response = requests.post(prefix + '/player/register', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def player_login(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix + '/player/login', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def player_update(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix + '/player/update', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def player_leaderboard(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix + '/player/leaderboard', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def prompt_create(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix + '/prompt/create', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def prompt_edit(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix + '/prompt/edit', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def prompt_delete(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix + '/prompt/delete', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def prompts_get(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    response = requests.post(prefix + '/prompts/get', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def prompts_getText(the_input, local=True):
    """
    the_input: as per specification
    local: if True, call the function on local development server at LOCAL_SERVER, if false, on the deployment at CLOUD_SERVER
    output: json as per the specification.
    """
    if local:
        prefix = LOCAL_SERVER
    else:
        prefix = CLOUD_SERVER
    print(prefix)
    response = requests.post(prefix + '/prompts/getText', json=the_input,
                             headers={'x-functions-key': APP_KEY})
    output = response.json()
    return output


def tests():
    # you may use this function for your own testing
    # You should remove your testing before submitting your CW
    print("Your own testing that you can call functions from here")

    # query = "SELECT * FROM players ORDER BY username ASC, total_score DESC"
    # query = 'SELECT TOP 3 * FROM (SELECT * FROM player p ORDER BY p.username ASC) as p2 ORDER BY p2.total_score DESC'
    # query = 'WITH p2 as (SELECT * FROM player p ORDER BY p.username ASC) SELECT * from p2 ORDER BY p2.total_score DESC'

    # players = player_database_functions.query_players("SELECT TOP 2 * FROM player p ORDER BY p.total_score desc, p.username asc")
    # for p in players:
    #     print(p['username'])


if __name__ == '__main__':
    # If the script is called from the console or inside an IDE
    # it will execute the tests function
    tests()
