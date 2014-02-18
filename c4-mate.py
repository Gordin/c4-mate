#!/usr/bin/env python3

import argparse
import urllib.request
from urllib.parse import quote
import re

me = ""

parser = argparse.ArgumentParser(description=
                                 'Add or subtract money from scratchcard.')
parser.add_argument('amount', type=float, nargs='*',
                    help='Amount to add or subtract')
parser.add_argument('-u', '--user', default=me,
                    help='Account to use. Defaults to "user" variable')
parser.add_argument('-t', '--to', required=False,
                    help='Account to transfer money to')

args = parser.parse_args()


def parse_mate(html, user=me):
    return re.match('.*' + user + ': (.*?)&', html, flags=re.DOTALL).group(1)


def perform_request(amount, user=me):
    if amount > 0:
        action = 'add'
    else:
        action = 'distract'
        amount = abs(amount)

    lichturl = "http://licht:8000/mate/" + quote(user)
    url = lichturl + "/" + action + "/?amount={}".format(amount)

    f = urllib.request.urlopen(url)
    if amount == 0:
        log_string = "Checking available money of {}".format(user)
    elif action == 'add':
        log_string = 'Added {}€ to {}'.format(amount, user)
    else:
        log_string = 'Subtracted {}€ from {}'.format(amount, user)

    print(log_string)
    return f.read().decode()


def check(user=me):
    response = perform_request(0)
    new_amount = parse_mate(response)
    print("{} has {}€".format(user, new_amount))
    return float(new_amount)


def transfer(user, to, amount):
    if amount <= 0:
        print("Transfer more that 0€ plz")
    elif check(user) < amount:
        print("{} doesn't have enough money to do this!".format(user))
    else:
        perform_request(amount, to)
        perform_request(-amount, user)


if not len(args.amount):
    check()

if args.to:
    for amount in args.amount:
        transfer(args.user, args.to, amount)
else:
    for amount in args.amount:
        if amount > 0 or check() + amount >= 0:
            response = perform_request(amount)
            new_amount = parse_mate(response)
            print("New Amount is {}€".format(new_amount))
        else:
            print("You don't have enough money to do this!")
