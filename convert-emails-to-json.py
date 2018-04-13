"""
This script is for use with the Auth0 import user extension. You can provide
a file that contains a list of e-mails which gets converted into a file
with a json object that the import user extension can read.
"""

import json
import argparse

parser = argparse.ArgumentParser(description='Convert e-mail list to JSON.')
parser.add_argument('--input-file',
    metavar='i',
    type=argparse.FileType('r'),
    default='invite.txt',
    nargs='+',
    help='the input file')

def to(e):
    return {
        "email" : e,
        "email_verified" : False
    }

args = parser.parse_args()
vard_args = vars(args)

f = vard_args['input_file'][0]

print(f)

if f:
    content = f.readlines()

print(content)
# with open(vard_args['input_file'] or "invite.txt") as f:
#     content = f.readlines()

content = [to(x.strip()) for x in content]

with open('invite.json', 'w') as outfile:
    json.dump(content, outfile)
