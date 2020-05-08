

from typing import Dict, List
import requests
from requests import Response

#Exception could be placed in submodule
class TicketingApiClientException(Exception):
    def __init__(self, response: Response):
        super().__init__(self)
        self.response = response


class TicketingApiUnexpectedStatusCodeException(TicketingApiClientException):
    pass


class TicketingApiMalformedResponseBodyException(TicketingApiClientException):
    pass

# Separating `urls` from ticketing project into importable module would allow importing valid URI instead of hardcoding them here
class TicketingApiClient:
    """Ticketing API client stub.

    You can expand it and add implementations
    to get data using different API endpoints.
    """

    URL = 'http://127.0.0.1:3000'

    def _extract_data(self, response, expected_status=200):
        if response.status_code != expected_status:
            raise TicketingApiUnexpectedStatusCodeException(response)
        try:
            return response.json()
        except ValueError:
            raise TicketingApiMalformedResponseBodyException(response)

    def get_orders(self, user_id: int = None) -> List[Dict]:
        """
        :raises TicketingApiUnexpectedStatusCodeException  server returned unexpected status code,
        :raises TicketingApiMalformedResponseBodyException response body is not a valid JSON
        """
        response = requests.get(f'{self.URL}/getOrders/{user_id}')
        return self._extract_data(response)

    def get_users(self) -> List[Dict]:
        """
        :raises TicketingApiUnexpectedStatusCodeException  server returned unexpected status code,
        :raises TicketingApiMalformedResponseBodyException response body is not a valid JSON
        """
        response = requests.get(f'{self.URL}/users/')
        return self._extract_data(response)

    def update_user(self, user_id, add_points=0):
        """
        :raises TicketingApiUnexpectedStatusCodeException  server returned unexpected status code,
        :raises TicketingApiMalformedResponseBodyException response body is not a valid JSON
        """
        response = requests.post(f'{self.URL}/update-user/', data=dict(user_id=user_id, add_points=add_points))
        return self._extract_data(response)