#!/usr/bin/env python3
import datetime
import gspread
import csv
import os
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
client_email = os.environ['GOOGLE_API_ACCOUNT']
user_email = os.environ['EMAIL_RECIPIENTS']
worksheet_key = os.environ['APPEND_GOOGLE_SHEET_KEY']


from io import StringIO


def create_new_report(json_creds, sheet_name, s3_data):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
    client = gspread.authorize(creds)
    gc = gspread.service_account_from_dict(json_creds)
    sh = gc.create(sheet_name)
    sh.share(user_email, perm_type='user', role='writer')
    gc.import_csv(sh.id, s3_data)
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/%s" % sh.id
    worksheet_list = sh.worksheets()
    print(worksheet_list)
    print("""

        Output:

    """)
    print(spreadsheet_url)


def update_existing_report(json_creds, s3_data):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
    client = gspread.authorize(creds)
    gc = gspread.service_account_from_dict(json_creds)
    sh = gc.open_by_key(worksheet_key)
    ws = sh.get_worksheet(0)
    f = open("query.csv", "w")
    f.write(s3_data)
    f.close()
    content = list(csv.reader(open('query.csv')))
    ws.append_rows(content, value_input_option="USER_ENTERED")
    os.remove('query.csv')
