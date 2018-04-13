"""
A management class for the Auth0 Management API. Right now it can create
and delete users. Made to be framework agnostic.
"""

import json
import requests
import string
import random
import urllib

class Auth0Management():
    def __init__(self, **kwargs):
        """
        Set the client_id, client_secret, domain, and audience,
        as well as initiating the access token needed.
        """
        self.client_id = kwargs['client_id']
        self.client_secret = kwargs['client_secret']
        self.domain = kwargs['domain']
        self.audience = kwargs['audience']

        self.base_url = "https://{domain}".format(domain=self.domain)
        self.users_endpoint = self.base_url + "/api/v2/users"
        self.tickets_password_change_endpoint = self.base_url + "/api/v2/tickets/password-change"

        self.access_token = self.get_auth0_access_token()
        self.api_headers = self.create_auth0_headers(self.access_token)

    def get_auth0_access_token(self, **kwargs):
        """
        Gets the auth0 access token with the class' client ID, secret, and audience.
        """
        payload = {
            "grant_type":"client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience
        }

        oauth_headers = { "content-type": "application/json" }

        r = requests.post(self.base_url + "/oauth/token", data=json.dumps(payload), headers=oauth_headers)
        r.raise_for_status()
        access_token = r.json()['access_token']

        return access_token

    def create_auth0_headers(self, access_token):
        """
        Creates the access token header.
        """
        api_headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        return api_headers

    def check_if_user_exists(self, email):
        """
        Checks if a user with `email` exists on the API
        """
        search = "q=" + urllib.parse.quote_plus("email:\"{email}\"".format(email=email))

        r = requests.get(self.users_endpoint,
            params=search,
            headers=self.api_headers
        )
        r.raise_for_status()

        return r.json()

    def create_user(self, email):
        """
        Will first check if the user exists, and if they don't will
        create them.
        """
        user_found = self.check_if_user_exists(email)
        if len(user_found) > 0:
            # User already exists
            return (False, user_found[0])
        user_payload = {
            "connection": "Username-Password-Authentication",
            "email": email,
            "password": ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)),
            "verify_email": False
        }

        r = requests.post(self.users_endpoint,
            headers=self.api_headers,
            data=json.dumps(user_payload)
        )

        r.raise_for_status()

        return (True, r.json())

    def delete_user(self, email):
        """
        Delete the user if they exist, finding them by their email address.
        """
        users = self.check_if_user_exists(email)
        if (len(users) == 0):
            # User doesn't exist
            return False
        elif (len(users) > 1):
            # Multiple users with e-mail address exist (???)
            return False
        # We have to do some unfolding to get the user's identity id
        r = requests.delete(self.users_endpoint + "/" + users[0]['user_id'],
            headers=self.api_headers)

        r.raise_for_status()

        return r.status_code == 204

    def create_password_change_ticket(self, user, result_url):

        ticket_payload = {
          "result_url": result_url,
          "user_id": user['user_id']
        }

        r = requests.post(self.tickets_password_change_endpoint,
            headers=self.api_headers,
            data=json.dumps(ticket_payload))

        r.raise_for_status()

        return r.json()

"""
for example usage in a Django app, in settings.py we'd need:

```
AUTH0 = {
    'DOMAIN': '',
    'AUDIENCE': '',
    'CLIENT_ID': '',
    'CLIENT_SECRET': ''
}
```

usage:
```
from auth0_management import Auth0Management

auth0 = Auth0Management(
    domain=settings.AUTH0['DOMAIN'],
    audience=settings.AUTH0['AUDIENCE'],
    client_id=settings.AUTH0['CLIENT_ID'],
    client_secret=settings.AUTH0['CLIENT_SECRET']
)

print(auth0.create_user('email'))
```
"""
