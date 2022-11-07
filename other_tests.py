import json
import unittest

import wrapper


# pytest ./tests/other_tests.py -s
class TestFunction(unittest.TestCase):

    def test_player_register(self):
        outputs = {
            'bad_uname': (False, 'Username less than 4 characters or more than 16 characters'),
            'bad_pass': (False, 'Password less than 8 characters or more than 24 characters'),
            'already_exists': (False, 'Username already exists'),
            'pass': (True, 'OK')
        }
        inputs = {
            "short_uname": {'username': 'no', 'password': '12345678'},
            "long_uname": {'username': 'this_is_a_very_very_long_username', 'password': '12345678'},
            "short_password": {'username': 'username', 'password': 'no'},
            "long_password": {'username': 'username', 'password': 'this_is_a_very_very_long_password'},
            "valid_input": {'username': 'username', 'password': '12345678'}
        }

        try:
            self.attempt_test(wrapper.player_register, inputs['short_uname'], outputs['bad_uname'])
            self.attempt_test(wrapper.player_register, inputs['long_uname'], outputs['bad_uname'])
            self.attempt_test(wrapper.player_register, inputs['short_password'], outputs['bad_pass'])
            self.attempt_test(wrapper.player_register, inputs['long_password'], outputs['bad_pass'])
        except Exception as e:
            self.fail(e)

    def attempt_test(self, method, dict_input, expected_output):
        final_output = {'result': expected_output[0], 'msg': expected_output[1]}
        self.assertEqual(method(dict_input), final_output)
