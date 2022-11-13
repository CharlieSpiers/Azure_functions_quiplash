import random
import string
import unittest

import wrapper


# pytest ./tests/player_tests.py -s
class TestFunction(unittest.TestCase):

    TEST_LOCALLY = False

    def attempt_test(self, method, dict_input, expected_output):
        final_output = {'result': expected_output[0], 'msg': expected_output[1]}
        self.assertEqual(final_output, method(dict_input, self.TEST_LOCALLY))

    def test_player_register(self):
        inputs = {
            "short_uname": {'username': random_string(3), 'password': '12345678'},
            "long_uname": {'username': random_string(17), 'password': '12345678'},
            "short_password": {'username': 'username', 'password': random_string(7)},
            "long_password": {'username': 'username', 'password': random_string(25)},
            "valid_input": {'username': random_string(8), 'password': 'test_password'}
        }
        outputs = {
            'bad_uname': (False, 'Username less than 4 characters or more than 16 characters'),
            'bad_pass': (False, 'Password less than 8 characters or more than 24 characters'),
            'already_exists': (False, 'Username already exists'),
            'pass': (True, 'OK')
        }

        try:
            register = wrapper.player_register
            self.attempt_test(register, inputs['short_uname'], outputs['bad_uname'])
            self.attempt_test(register, inputs['long_uname'], outputs['bad_uname'])
            self.attempt_test(register, inputs['short_password'], outputs['bad_pass'])
            self.attempt_test(register, inputs['long_password'], outputs['bad_pass'])
            self.attempt_test(register, inputs['valid_input'], outputs['pass'])
            self.attempt_test(register, inputs['valid_input'], outputs['already_exists'])
        except Exception as e:
            self.fail(e)

    def test_player_login(self):
        inputs = {
            'random_user': {'username': random_string(8), 'password': random_string(12)}
        }
        outputs = {
            'bad_creds': (False, 'Username or password incorrect'),
            'pass': (True, 'OK')
        }
        try:
            login = wrapper.player_login
            self.attempt_test(login, inputs['random_user'], outputs['bad_creds'])
            wrapper.player_register(inputs['random_user'], self.TEST_LOCALLY)
            self.attempt_test(login, inputs['random_user'], outputs['pass'])
        except Exception as e:
            self.fail(e)

    def test_player_update(self):
        random_username = random_string(8)
        inputs = {
            'random_user': {'username': random_username, 'password': random_string(12), "add_to_score": 1, "add_to_games_played": 1},
            'random_user_bad_pass': {'username': random_username, 'password': '', "add_to_score": 1},
            'random_user_bad_score': {'username': random_username, 'password': '', "add_to_score": -1},
            'random_user2': {'username': random_string(8), 'password': '', "add_to_score": 1}
        }
        outputs = {
            'user_not_exists': (False, 'user does not exist'),
            'bad_value': (False, 'Value to add is <=0'),
            'bad_password': (False, 'wrong password'),
            'pass': (True, 'OK')
        }
        try:
            update = wrapper.player_update
            wrapper.player_register(inputs['random_user'], self.TEST_LOCALLY)
            self.attempt_test(update, inputs['random_user'], outputs['pass'])
            self.attempt_test(update, inputs['random_user_bad_pass'], outputs['bad_password'])
            self.attempt_test(update, inputs['random_user_bad_score'], outputs['bad_value'])
            self.attempt_test(update, inputs['random_user2'], outputs['user_not_exists'])
        except Exception as e:
            self.fail(e)


def random_string(num):
    return ''.join(random.choice(string.ascii_letters) for i in range(num))


# python ./tests/player_tests.py
# For manual tests e.g. leaderboard
if __name__ == "__main__":
    print(wrapper.player_leaderboard({"top": 4}))
