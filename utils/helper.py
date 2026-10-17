from typing import TypeVar
import json
import allure
import requests
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class Helper:

    @staticmethod
    def attach_response(response_body):
        perfect_response = json.dumps(
            response_body,
            indent=4,
            ensure_ascii=False
        )

        allure.attach(
            body=perfect_response,
            name="API Response",
            attachment_type=allure.attachment_type.JSON
        )

    def validate_response(
        self,
        response: requests.Response,
        model: type[T] | None = None,
        expected_status_code: int = 200
    ) -> T | None:

        try:
            response_body = response.json()
            self.attach_response(response_body)
        except ValueError:
            response_body = None

        assert response.status_code == expected_status_code, (
            f"Expected status code {expected_status_code}, "
            f"but received {response.status_code}. "
            f"Response: {response_body}"
        )

        if model is None:
            return None

        if isinstance(response_body, dict):
            return model(**response_body)

        if isinstance(response_body, list):
            return [model(**item) for item in response_body]

        raise AssertionError(
            f"Unexpected response body type: {type(response_body).__name__}"
        )