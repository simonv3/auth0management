import requests
import settings

def send_onboard_email(to_user):
    r = requests.post(
        settings.MAILGUN['API'],
        auth=("api", settings.MAILGUN['API_KEY']),
        data={"from": settings.MAILGUN['FROM'],
              "to": to_user['email'],
              "subject": settings.ONBOARDING['SUBJECT'],
              "text": settings.ONBOARDING['TEXT']
        })

    print('\t', r.json()['message'])
    r.raise_for_status()
