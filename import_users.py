"""
A script that uses the Auth0Management module to import emails supplied
to the script directly or as a list in an input file
"""

from auth0_management import Auth0Management
import argparse

import settings
import send_email

parser = argparse.ArgumentParser(description='Import a specific e-mail.')
parser.add_argument('--email',
    metavar='e',
    type=str,
    help='a specific e-mail to import')
parser.add_argument('--input-file',
    metavar='i',
    type=argparse.FileType('r'),
    help='the input file')
parser.add_argument('--send-onboard',
    action='store_true',
    help="specify if the password for the just created user should be reset and an pnboard email sent")

auth0 = Auth0Management(
    domain=settings.AUTH0['DOMAIN'],
    audience=settings.AUTH0['AUDIENCE'],
    client_id=settings.AUTH0['CLIENT_ID'],
    client_secret=settings.AUTH0['CLIENT_SECRET']
)

args = parser.parse_args()
vard_args = vars(args)

def onboard_user(user_success_object):
    print(user_success_object)
    (success, user) = user_success_object
    ticket = auth0.create_password_change_ticket(user, settings.RESULT_URL)
    send_email.send_onboard_email(user)

if ('email' in vard_args and vard_args['email']):
    email = vard_args['email']

    user_success_object = auth0.create_user(email)

    if 'send_onboard' in vard_args and vard_args['send_onboard']:
        onboard_user(user_success_object)

if ('input_file' in vard_args):
    f = vard_args['input_file']

    if f:
        content = [line.strip() for line in f.readlines()]
        success = [auth0.create_user(email) for email in content]

        if 'send_onboard' in vard_args and vard_args['send_onboard']:
            for user_success_object in success:
                onboard_user(user_success_object)
