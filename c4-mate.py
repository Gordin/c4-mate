#!/usr/bin/env python3

import argparse
import urllib.request
import re

parser = argparse.ArgumentParser(description=
                                 'Add or subtract money from scratchcard.')
parser.add_argument('amount', type=float, nargs='+',
                    help='Amount to add or subtract')

user = ""
lichturl = "http://licht:8000/mate/" + user
args = parser.parse_args()


def parse_mate(html):
    return re.match('.*' + user + ': (.*?)&', html, flags=re.DOTALL).group(1)

for amount in args.amount:

    if amount > 0:
        action_strings = {'url': 'add', 'text': 'Added'}
    else:
        action_strings = {'url': 'distract', 'text': 'Subtracted'}
        amount = abs(amount)

    url = lichturl + "/" + action_strings['url'] + "/?amount={}".format(amount)
    f = urllib.request.urlopen(url)
    print(action_strings['text'] + " {}€".format(amount))

    response = f.read().decode()
    new_amount = parse_mate(response)
    print("New Amount is {}€".format(new_amount))
