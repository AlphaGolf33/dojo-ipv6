#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import sys
import os
import subprocess
import pickle
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


FILE_PATH = os.path.dirname(os.path.realpath(__file__))
STORAGE_PATH = os.path.join(FILE_PATH, 'storage.txt')
CREDENTIALS_PATH = os.path.join(FILE_PATH, 'credentials.json')
TOKEN_PATH = os.path.join(FILE_PATH, 'token.pickle')
OAUTH2_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1xiTpQ5WG0K1fqQtWB4hTM1HGhejqvxnhp8CMKBi7w2o'


def was_people_connected():
    if (not os.path.isfile(STORAGE_PATH)):
        return False

    with open(STORAGE_PATH, 'r') as f:
        return f.readline(1) == '1'


def is_people_connected():
    cmd = subprocess.run(['who', '--count'], capture_output=True)
    count = int(cmd.stdout.strip().decode()[-1:])
    return count > 0


def save_people_connected(is_connected):
    with open(STORAGE_PATH, 'w') as f:
        f.write(str(int(is_connected)))


def get_google_creds():
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, OAUTH2_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def update_sheet(creds, index, is_connected):
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'requests': [
            {
                'updateCells': {
                    'fields': 'userEnteredFormat',
                    'range': {
                        'sheetId': 0,
                        'startColumnIndex': 1,
                        'endColumnIndex': 2,
                        'startRowIndex': index,
                        'endRowIndex': index + 1
                    },
                    'rows': [
                        {
                            'values': [
                                {
                                    'userEnteredFormat': {
                                        'backgroundColor': {
                                            'red': 0 if is_connected else 1,
                                            'green': 1 if is_connected else 0,
                                            'blue': 0
                                        },
                                        'horizontalAlignment': 'CENTER',
                                        'borders': {
                                            'bottom': {
                                                'style': 'NONE' if index % 2 else 'SOLID'
                                            },
                                            'left': {
                                                'style': 'SOLID'
                                            },
                                            'right': {
                                                'style': 'SOLID'
                                            },
                                            'top': {
                                                'style': 'SOLID' if index % 2 else 'NONE'
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }

    request = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body)
    request.execute()


def update(index):
    is_connected = is_people_connected()
    if is_connected == was_people_connected():
        return

    save_people_connected(is_connected)
    creds = get_google_creds()
    update_sheet(creds, index, is_connected)


def main():
    if sys.version_info[0] < 3:
        print('ERROR: This program requires at least python 3')
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('index', metavar='VM_NUMBER', type=int,
                        help='Index of the VM, e.g. dojo1 = 1')
    args = parser.parse_args()

    while True:
        update(args.index)
        time.sleep(3)


if __name__ == '__main__':
    main()
