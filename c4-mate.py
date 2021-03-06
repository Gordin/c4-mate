#!/usr/bin/env python3

import argparse
import urllib.request
from urllib.parse import quote
import re

me = ""

parser = argparse.ArgumentParser(
    description='Add or subtract money from scratchcard.')
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
        action = 'subtract'
        amount = abs(amount)

    lichturl = "http://autoc4/mate/user/" + quote(user)
    url = lichturl + "/" + action + "/{}".format(amount)

    try:
        f = urllib.request.urlopen(url)
    except:
        print("Beim Aufruf ist ein Fehler aufgetreten.\nDer Zugriff wird beendet.\nMögliche Fehler: server nicht erreichbar, Nutzername existiert nicht in der gegebenen Schreibweise")
        raise SystemExit

    if amount == 0:
        log_string = "Checking available money of {}".format(user)
    elif action == 'add':
        log_string = 'Added {}€ to {}'.format(amount, user)
    else:
        log_string = 'Subtracted {}€ from {}'.format(amount, user)

    print(log_string)
    return f.read().decode()


def give(user, to, amount):
    url = "http://autoc4/mate/user/{}/give/{}/to/{}".format(quote(user),
                                                            amount, quote(to))

    log_string = "Giving {}€ from {} to {}.".format(amount, user, to)
    print(log_string)

    f = urllib.request.urlopen(url)

    return f.read().decode()


def check(user=me):
    response = perform_request(0, user)
    new_amount = parse_mate(response, user)
    print("{} has {}€".format(user, new_amount))
    return float(new_amount.replace(',', '.'))


def transfer(user, to, amount):
    if amount <= 0:
        print("Transfer more than 0€ plz")
    elif check(user) < amount:
        print("{} doesn't have enough money to do this!".format(user))
    else:
        return give(user, to, amount)


def do_transaction(user, to, amount):
    if amount > 0 or check(user) + amount >= 0:
        if to:
            response = transfer(user, to, amount)
            check(user)
        else:
            response = perform_request(amount, args.user)
            new_amount = parse_mate(response)
            print("New Amount is {}€".format(new_amount))
    else:
        print("You don't have enough money to do this!")


def main():
    if not len(args.amount):
        return check(args.user)

    if not args.user:
        args.user = me

    for amount in args.amount:
        do_transaction(args.user, args.to, amount)

if __name__ == '__main__':
    main()
