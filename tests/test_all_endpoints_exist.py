import unittest
import requests


# pytest ./tests/test_all_endpoints_exist.py -s
# -s allows the print() to work, otherwise it doesn't
class TestFunction(unittest.TestCase):
    endpoints = [
        "player/leaderboard",
        "player/login",
        "player/register",
        "player/update",
        "prompt/create",
        "prompt/delete",
        "prompt/edit",
        "prompts/get",
        "prompts/getText"
    ]

    def test_all_endpoints_exist(self):
        for endpoint in self.endpoints:
            uri = f"http://localhost:7071/api/{endpoint}"
            resp = requests.get(uri)
            print(f"testing: {endpoint}")

            self.assertNotEqual(resp.status_code, 404)
