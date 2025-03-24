import json
from unittest.mock import Mock


class MockBackendService:
    def __init__(self, test_data_file: str = None):
        with open(test_data_file) as file:
            self.test_data = json.load(file)

    def authenticate(self, username, password):
        return self.__test_response(200, self.test_data["authenticate_response"])

    def get_movies(self):
        return self.__test_response(201, self.test_data["movies"])

    def __test_response(self, status_code, data):
        test_response = Mock()
        test_response.status_code = status_code
        test_response.json.return_value = data
        return test_response
