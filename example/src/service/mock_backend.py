import json
from unittest.mock import Mock
import random


class MockBackendService:
    def __init__(self, test_data_file: str = None):
        with open(test_data_file) as file:
            self.test_data = json.load(file)

    def authenticate(self, username: str, password: str):
        if username and password:
            return self.__test_response(200, self.test_data["authenticate_response"])
        return self.__test_response(403, {})

    def get_movies(self):
        data = self.test_data["movies"]
        rating = random.randint(1, 10)
        for item in data:
            item["rating"] = rating
        return self.__test_response(201, data)

    def __test_response(self, status_code, data):
        test_response = Mock()
        test_response.status_code = status_code
        test_response.json.return_value = data
        test_response.ok = 200 <= test_response.status_code < 400
        return test_response
