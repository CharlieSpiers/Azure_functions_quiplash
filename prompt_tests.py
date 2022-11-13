import random
import string
import unittest

import wrapper


# pytest .\prompt_tests.py -s
class TestFunction(unittest.TestCase):

    TEST_LOCALLY = False

    def attempt_test(self, method, dict_input, expected_output):
        final_output = {'result': expected_output[0], 'msg': expected_output[1]}
        self.assertEqual(final_output, method(dict_input, self.TEST_LOCALLY))

    def test_prompt_create(self):
        random_username = random_string(8)
        random_password = random_string(12)
        inputs = {
            "random_user1": {'username': random_username, 'password': random_password, 'text': random_string(20)},
            "bad_text1": {'username': random_username, 'password': random_password, 'text': random_string(19)},
            "bad_text2": {'username': random_username, 'password': random_password, 'text': random_string(101)}
        }
        outputs = {
            'same_text': (False, 'This user already has a prompt with the same text'),
            'prompt_length': (False, 'prompt length is <20 or > 100 characters'),
            'bad_creds': (False, 'bad username or password'),
            'pass': (True, 'OK')
        }

        try:
            create = wrapper.prompt_create
            self.attempt_test(create, inputs['random_user1'], outputs['bad_creds'])
            wrapper.player_register(inputs["random_user1"], self.TEST_LOCALLY)
            self.attempt_test(create, inputs['random_user1'], outputs['pass'])
            self.attempt_test(create, inputs['random_user1'], outputs['same_text'])
            self.attempt_test(create, inputs['bad_text1'], outputs['prompt_length'])
            self.attempt_test(create, inputs['bad_text2'], outputs['prompt_length'])
        except Exception as e:
            self.fail(e)

    def test_prompt_edit_and_delete(self):
        uname = random_string(8)
        password = random_string(12)
        inputs = {
            'random_user': {'username': uname, 'password': password, 'text': random_string(20), 'id': 0},
            'bad_prompt_len': {'username': uname, 'password': password, 'text': random_string(19), 'id': 0}
        }
        outputs = {
            'bad_pid': (False, 'prompt id does not exist'),
            'bad_prompt_length': (False, 'prompt length is <20 or >100 characters'),
            'repeated_prompt': (False, 'This user already has a prompt with the same text'),
            'bad_creds': (False, 'bad username or password'),
            'pass': (True, 'OK')
        }
        try:
            edit = wrapper.prompt_edit
            self.attempt_test(edit, inputs['random_user'], outputs['bad_creds'])
            wrapper.player_register(inputs["random_user"], self.TEST_LOCALLY)
            self.attempt_test(edit, inputs['random_user'], outputs['bad_pid'])
            self.attempt_test(wrapper.prompt_delete, inputs['random_user'], outputs['bad_pid'])

            wrapper.prompt_create(inputs['random_user'], self.TEST_LOCALLY)
            id1 = int(wrapper.prompts_get({'players': [uname]}, self.TEST_LOCALLY)[0]['id'])
            inputs['random_user']['id'] = id1
            inputs['bad_prompt_len']['id'] = id1

            self.attempt_test(edit, inputs['random_user'], outputs['repeated_prompt'])
            self.attempt_test(edit, inputs['bad_prompt_len'], outputs['bad_prompt_length'])

            inputs['random_user']['text'] = "This is a text used to test the prompt edit can complete"
            self.attempt_test(edit, inputs['random_user'], outputs['pass'])

            self.attempt_test(wrapper.prompt_delete, inputs['random_user'], outputs['pass'])
        except Exception as e:
            self.fail(e)


def random_string(num):
    return ''.join(random.choice(string.ascii_letters) for i in range(num))


# python .\prompt_tests.py
# For manual tests
if __name__ == "__main__":
    print(wrapper.prompts_get({"prompts": 4}))
    print(wrapper.prompts_getText({"word": 'The', 'exact': False}))
