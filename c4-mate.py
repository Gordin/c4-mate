#!/usr/bin/env python3

import argparse
import urllib.request
from urllib.parse import quote
import re

parser = argparse.ArgumentParser(description=
                                 'Add or subtract money from scratchcard.')
parser.add_argument('amount', type=float, nargs='*',
                    help='Amount to add or subtract')

user = ""
lichturl = "http://licht:8000/mate/" + quote(user)
args = parser.parse_args()


def parse_mate(html):
    return re.match('.*' + user + ': (.*?)&', html, flags=re.DOTALL).group(1)


def perform_request(amount):
    if amount > 0:
        action_strings = {'url': 'add', 'text': 'Added'}
    else:
        action_strings = {'url': 'distract', 'text': 'Subtracted'}
        amount = abs(amount)

    url = lichturl + "/" + action_strings['url'] + "/?amount={}".format(amount)

    f = urllib.request.urlopen(url)
    if amount == 0:
        log_string = "Checking available money"
    else:
        log_string = action_strings['text'] + " {}€".format(amount)

    print(log_string)
    return f.read().decode()


def check():
    response = perform_request(0)
    new_amount = parse_mate(response)
    print("Current Amount is {}€".format(new_amount))
    return float(new_amount)


if not len(args.amount):
    check()

for amount in args.amount:
    if amount > 0 or check() + amount >= 0:
        response = perform_request(amount)
        new_amount = parse_mate(response)
        print("New Amount is {}€".format(new_amount))
    else:
        print("You don't have enough money to do this!")
