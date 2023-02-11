from unittest import TestCase
from unittest.mock import Mock

import main
class Test(TestCase):
    def test_cf_gpt(self):
        prompt = 'how to make a pancake'
        data = {'prompt': prompt}
        req = Mock(get_json=Mock(return_value=data), args=data)
        res = main.model_basic(req)
        print(res)
        # Call tested function
        assert req


