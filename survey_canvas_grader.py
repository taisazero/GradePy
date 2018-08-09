from __future__ import print_function
from tkinter import *
import pandas as pd
import os
import collections
from nltk.metrics import edit_distance as ed
from openpyxl import load_workbook
import csv

import httplib2

# import google api reqs
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import math
from canvasapi.canvas import Canvas

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

participant_list=[]


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def read_participants():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = input('Spreadsheet ID: ')
    rangeName = 'Form Responses 1!A1:B250'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Success!')

        return values



def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def browse():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename


def getDir():
    from tkinter.filedialog import askdirectory
    Tk().withdraw()
    name = askdirectory()
    return name



def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False














for time_stamp,email in read_participants():
    if email!= 'Email Address':
       participant_list.append(email.replace('@uncc.edu',''))


print(
    'Due to the Canvas API\'s BS restrictions, we need to ask for the student logins file. Please Browse and select the student logins csv file.' +
    ' It needs to have the following columns : Student, ID, Login')
logins_file = browse()
df = pd.read_csv(logins_file, index_col=1)

user_dic={}
for row in range(0,len(df['Login'].keys())):
    user_dic[df['Login'][row]] = df['ID'][row]

id_list=[]
for student in participant_list:
    if student in user_dic.keys():
        id_list.append(user_dic[student])


API_URL = "https://uncc.instructure.com/"
# Canvas API key
file = open('token.txt', 'r')

API_KEY = str(file.read())
file.close()
# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

course = canvas.get_course(input('Enter course ID: '))

print('Grading the course : ' + course.name)

survey_assignment=course.get_assignment(input('Enter assignment ID: '))

submissions=survey_assignment.get_submissions()
total_points=float(survey_assignment.points_possible)
for submission in submissions:
    if submission.user_id in id_list:
        submission.edit(submission={'score':total_points})
    else:
        submission.edit(submission={'score':0.0})




