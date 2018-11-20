import argparse
import json
import os
import sys

from oldclient import OLDClient


OLD_URL_DFLT = 'http://127.0.0.1/'
OLD_USERNAME_DFLT = 'admin'
OLD_PASSWORD_DFLT = 'adminA_1'


def get_connection_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--old-url',
        type=str,
        dest='url',
        default=os.environ.get('OLD_URL', OLD_URL_DFLT),
        help='The URL of the Online Linguistic Database')
    parser.add_argument(
        '-u',
        '--username',
        type=str,
        dest='username',
        default=os.environ.get('OLD_USERNAME', OLD_USERNAME_DFLT),
        help='The username for authenticating to the OLD instance.')
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        dest='password',
        default=os.environ.get('OLD_PASSWORD', OLD_PASSWORD_DFLT),
        help='The password for authenticating to the OLD instance.')
    return vars(parser.parse_args())


def get_old_client(options):
    old_client = OLDClient(options['url'])
    try:
        assert old_client.login(options['username'], options['password'])
    except AssertionError:
        print('Unable to login to OLD instance {url} using username {username}'
              ' and password {password}.'.format(**options))
        sys.exit(1)
    return old_client


def create_test_form(old_client):
    form = old_client.models['form'].copy()
    form['transcription'] = 'Arma virumque cano.'
    form['translations'].append({
        'transcription': 'I sing of arms and a man.',
        'grammaticality': ''
    })
    response = old_client.create(
        'forms',
        data=form)
    print(f'{response["enterer"]["first_name"]} '
          f'{response["enterer"]["last_name"]} created a new form with '
          f'id {response["id"]} on {response["datetime_entered"]}.\n'
          f'See https://app.dative.ca/#form/{response["id"]}.')


def main():
    options = get_connection_options()
    old_client = get_old_client(options)
    create_test_form(old_client)


if __name__ == '__main__':
    main()
