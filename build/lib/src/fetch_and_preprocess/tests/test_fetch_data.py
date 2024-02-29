import unittest
from unittest.mock import Mock
import requests
from ..fetch_data import check_format_basic, fetch_data


class TestFetch(unittest.TestCase):

    def test_check_if_response_correct_invalid_format(self):
        # Invalid response format
        response = Mock()
        response.json.return_value = {'invalid_key': 'data'}
        response.raise_for_status.return_value = None
        self.assertFalse(check_format_basic(response))

    def test_check_if_response_correct_empty_result(self):
        # Response with empty data list
        response = Mock()
        response.json.return_value = {'result': []}
        response.raise_for_status.return_value = None
        self.assertFalse(check_format_basic(response))

    def test_check_if_response_correct_http_error(self):
        # Simulating HTTP error
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")
        self.assertFalse(check_format_basic(response))

    def test_fetch_data_success(self):
        # Successful fetch
        api_data = {'url': 'http://example.com', 'params': {}, 'headers': {}}
        with unittest.mock.patch('requests.get') as mocked_get:
            mocked_response = Mock(ok=True)
            mocked_get.return_value = mocked_response
            mocked_response.json.return_value = {'result': ['data']}
            self.assertIsNotNone(fetch_data(api_data))

    def test_fetch_data_failure(self):
        # Failed fetch
        api_data = {'url': 'http://example.com', 'params': {}, 'headers': {}}
        with unittest.mock.patch('requests.get') as mocked_get:
            mocked_response = Mock(ok=False, text="Error message")
            mocked_get.return_value = mocked_response
            self.assertIsNone(fetch_data(api_data))


if __name__ == '__main__':
    unittest.main()
