import requests
import settings
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('auth0_management', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def send_onboard_email(to_user, url):
    html_template = env.get_template(settings.ONBOARDING['HTML_TEMPLATE'])
    text_template = env.get_template(settings.ONBOARDING['TEXT_TEMPLATE'])

    r = requests.post(
        settings.MAILGUN['API'],
        auth=("api", settings.MAILGUN['API_KEY']),
        data={"from": settings.MAILGUN['FROM'],
              "to": to_user['email'],
              "subject": settings.ONBOARDING['SUBJECT'],
              "text": text_template.render(link=url, user=to_user),
              "html": html_template.render(link=url, user=to_user)
        })

    print('\t', r.json()['message'])
    r.raise_for_status()
