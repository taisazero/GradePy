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

absent_list=[]
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
def read_attendance():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1_NqJr3WLyPTso6rs5Zc55x-YIpENMWvPPgdwEXnKDLU'
    rangeName = 'Dorodchi!A1:B123'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Success!')




        return values


def update_attendance(values,absents):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1_NqJr3WLyPTso6rs5Zc55x-YIpENMWvPPgdwEXnKDLU'
    rangeName = 'Dorodchi!A1:B123'
    value_body = {}
    value_body['values'] = []
    print('absents: ',absents)
    if not values:
        print('No data found.')
    else:


        for row in values:

            if row[0] not in absents:
                value_body['values'].append([row[0], row[1]])
            else:
                while row[0] in absents:
                    num_abs=int(row[1]) + 1
                    value_body['values'].append([str(row[0]), str(num_abs)])
                    absents.remove(row[0])

    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, body=value_body,
                                                    key='AIzaSyA1aL_MNNzezE9NU2t93N9iqpubgx_MuVw',
                                                    valueInputOption='USER_ENTERED').execute()


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
    name=askdirectory()
    return name

print('Pick Gradebook')
grades=browse()
print('Pick directory for Kahoot csvs')
toAdd=getDir()
files=os.listdir(toAdd)
gradebook=pd.read_csv(grades)
print(gradebook.to_dict())
grade_dic = collections.defaultdict(lambda:collections.defaultdict(lambda:0))



def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def get_student(students, id):
    temp = 1000
    name = ''
    used_id=id
    id = id.lower()

    for num in range(0, len(students)):
        s = str(students[num])
        if (id.__contains__('@uncc.edu')):
            id = id[0:id.index('@')]
        if (id.__contains__(' ')):
            id = id[0:1] + id[id.index(' ') + 1:len(id)]
        if (s != None and not s == 'nan' and id != None):
            try:
                if (ed(s, id) == 0):

                    return s, used_id
                elif temp > ed(s, id):
                    temp = ed(s, id)
                    name = s
            except TypeError:
                print(id)
    if (temp / len(name) <= 0.35):
        #print(id, name, temp / len(name))
        return name, used_id
    else:

        return None, used_id


def get_student2(kahooters, students):
    correct = 0
    incorrect = 0
    total = 0
    dic = {}
    not_found = set()
    for s1 in students:
        s1 = s1.lower()
        temp = 1000
        name = 'abc '
        target= ''
        for num in kahooters:

            s = str(num)
            used_kahoot = s

            s = s.lower()
            if (s.__contains__('@')):
                s = s[0:s.index('@')]
            if (s.__contains__(' ')):
                s = s[0:1] + s[s.index(' ') + 1:len(s)]

            if (s != None and not s == 'nan' and students != None):

                try:




                    if temp > ed(s, s1):
                        temp = ed(s, s1)
                        name = s1
                        target=used_kahoot

                        if (temp == 0 or temp ==1):
                            name = s1
                            dic[s1] = [name, used_kahoot, temp]
                            correct += 1

                            break

                except TypeError:
                    print()


        if ( temp / len(name) <= 0.4 and temp < len(name)):
            # print( name,used_id, temp / len(name))
            dic[s1] = [name, target, temp]

            if used_kahoot in kahooters:
                kahooters.remove(used_kahoot)

            if name == s1:
                correct += 1
            else:
                print('Incorrect: ',s1, target, temp)
                incorrect += 1
        else:
            not_found.add(used_kahoot)


            # total+=1
    print('Accuracy is ' + str(float(correct / (correct+total+incorrect)) * 100) + '%')
    print(not_found)
    return dic

def readFiles():



    list_files=[]

    list_students = []
    for num in range(1, len(gradebook['SIS Login ID'])):
        list_students.append(str(gradebook['SIS Login ID'][num]))


    for file in files:

        new_grades=pd.read_csv(toAdd+'\\'+file)
        list_files.append(str(file[0:file.index('.csv')]))

        list_kahooters=[]
        for i in range(0,len(new_grades['Players'])):
            s = str(new_grades['Players'][i])
            if (s!= None):
                list_kahooters.append(s)
        assignment_name = str(file[0:file.index('.csv')])
        """
        for i in range (0,len(list_students)):
            temp_kahooter,temp_student=get_student2(list_kahooters,list_students[i])
            print(temp_kahooter,list_students[i])
            if temp_kahooter!=list_students[i] or temp_kahooter == None:
                grade_dic[temp_student][assignment_name]=0
                absent_list.append(list_students[i])

        """
        id_kahoot_dic=get_student2(list_kahooters,list_students)
        """
        for index in range(0,len(list_kahooters)):

            student=str(list_kahooters[index])
            if (student!=None):
                student,id=get_student(list_students,student)


            if(student in list_kahooters):
                grade_dic[student][assignment_name]=new_grades['Correct Answers'][new_grades.index[new_grades['Players']==id][0]]
        """
        for student in list_students:
            if (student in id_kahoot_dic.keys()):
                if id_kahoot_dic[student][0]!=None:
                    kahoot_id=id_kahoot_dic[student][1]
                    grade_dic[assignment_name][student] = new_grades['Correct Answers'][
                        new_grades.index[new_grades['Players'] == kahoot_id][0]]
            else:
                grade_dic[assignment_name][student] = 0
                absent_list.append(student)
        update_gradebook(grade_dic[assignment_name],assignment_name)


    print('absents: ',absent_list)
    return list_files,grade_dic


def write_summary(list_files):
    stuff = open('C:\\Users\\Zero\\Documents\\Kahoot workspace\\summary.csv', 'w')
    stuff.write('Name,')

    total_points = float(input('Enter total points possible '))

    for assignment in list_files:
        stuff.write(assignment + ',')
    stuff.write('total,')
    stuff.write('%,')

    for assignment in grade_dic.keys():
        total = 0


        for student in grade_dic[assignment].keys():
            stuff.write('\n')
            stuff.write(str(student) + ',')
            stuff.write(str(grade_dic[assignment][student]) + ',')
            total += grade_dic[assignment][student]
        stuff.write(str(total) + ',')
        stuff.write(str(float(total / total_points) * 100) + '%' + ',')

    stuff.close()
"""
def get_attendance_list(grades,list_files):
    
    print ('List files is : ',len(list_files))
    for student in grades.keys():
       print(grades[student].keys())
       num_absent=len(list_files) - len(grades[student].keys())
       for i in range(0,num_absent):
           absent_list.append(student)
    return absent_list
"""




def get_totals(grade_dic):
    totals=collections.defaultdict(lambda:0)
    for assignment in grade_dic.keys():
        total=0
        for student in grade_dic[assignment].keys():
            total += grade_dic[assignment][student]
        totals[student]=total
    return totals
def update_gradebook(grade_dic,assignment):
    #total_grades=pd.DataFrame.from_dict(get_totals(grade_dic))
    panda=pd.read_csv(grades)
    reader=panda.to_dict()
    key=input('Enter Kahoot ID for ' + assignment + ' ')
    for student in grade_dic.keys():
        if student != 'nan' and student!= None and student!= '':

            reader[key][panda.index[gradebook['SIS Login ID'] == student][0]]=grade_dic[student]
    new_file=open(grades,'w')
    writer=csv.DictWriter(new_file,reader.keys())
    writer.writeheader()
    print(reader[key])

    for index in range(0, len(reader['Student'].keys())):
        row = []
        for key in reader:

            if (key!=0 and isint(key) == False and isfloat(key)== False and reader[key][index]!='nan' and reader[key][index]!=None and reader[key][index]!=''):
                new_file.write(str(reader[key][index])+',')
            else:
                new_file.write('\t,')
        new_file.write('\n')
    new_file.close()


#Kahoot 1.1 (302069)
#Kahoot 1.2 (302070)
#Kahoot 2.1 (302071)
#Kahoot-2.2 (302072)
#Kahoot-3.0 (302073)
#Kahoot-3.1 (302074)
#Kahoot -3.5 (302075)
#Kahoot 3.2 (350341)



list_files,grade_dic=readFiles()

write_summary(list_files)

a_data=read_attendance()
update_attendance(a_data,absent_list)

