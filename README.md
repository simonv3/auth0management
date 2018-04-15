This is a Auth 0 Management API wrapper class that lets you add and delete users
from Auth0.

It uses python3.

To install:

```
git clone git@github.com:simonv3/auth0management.git
cd auth0management
pip3 install -r requirements.txt
```

(this is just the `requests` library at the moment)

And then:

```
python3 import_users.py --email=<email>
```

or

```
python3 import_users.py --input-file=<file-location>
```

### Sending Emails After Creating a User

If you want to create a user and send them an onboard e-mail, you need to set
up an e-mail provider for it. Right now the script relies on Mailgun, but other
email providers could be added fairly easily.

Once that's set up (in settings.py) you can add the --send-onboard option
to the API calls.

```
python3 import_users.py --email=<email> --send-onboard
```
