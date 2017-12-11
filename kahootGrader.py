from tkinter import *
import nltk
import pandas as pd
import os
import collections
from nltk.metrics import edit_distance as ed
from openpyxl import load_workbook
import math
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
grade_dic = collections.defaultdict(lambda:collections.defaultdict(lambda:0))



def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def get_student(students,id):


    temp=1000
    name=''

    for s in students:
        s=str(s)
        if(s!=None and not isfloat(s) and not isint(s) and not s=='nan'):
            try:
                if(ed(s,id)==0):
                    return s
                elif temp>ed(s,id):
                    temp=ed(s,id)
                    name=s
            except TypeError:
                print (s)
    if(temp<=4 and  len(name)>4):
        print(id, name, temp)
        return name
    else:

        return None

def readFiles():



    list_files=[]



    for file in files:

        new_grades=pd.read_csv(toAdd+'\\'+file)
        list_files.append(str(file[0:file.index('.csv')]))

        assignment_name=str(file[0:file.index('.csv')])
        for num in range(0, len(gradebook['SIS Login ID'])-1):
            grade_dic[gradebook['SIS Login ID'][num]][assignment_name]=0
        for index in range(0,len(new_grades['Players'])-2):

            student=str(new_grades['Players'][index]).lower()
            if(get_student(list(grade_dic.keys()),student)!=None):
                grade_dic[get_student(list(grade_dic.keys()),student)][assignment_name]=new_grades['Correct Answers'][index]
    return list_files,grade_dic


def write_summary(list_files):
    stuff = open('summary.csv', 'w')
    stuff.write('Name,')

    total_points = float(input('Enter total points possible '))

    for assignment in list_files:
        stuff.write(assignment + ',')
    stuff.write('total,')
    stuff.write('%,')

    for student in grade_dic.keys():
        total = 0
        stuff.write('\n')
        stuff.write(str(student) + ',')

        for assignment in grade_dic[student].keys():
            stuff.write(str(grade_dic[student][assignment]) + ',')
            total += grade_dic[student][assignment]
        stuff.write(str(total) + ',')
        stuff.write(str(float(total / total_points) * 100) + '%' + ',')

    stuff.close()

def get_totals(grade_dic):
    totals=collections.defaultdict(lambda:0)
    for student in grade_dic.keys():
        total=0
        for assignment in grade_dic[student].keys():
            total += grade_dic[student][assignment]
        totals[student]=total
    return totals
#todo
def update_gradebook(grade_dic):
    total_grades=pd.DataFrame.from_dict(get_totals(grade_dic))
    reader=pd.read_csv(grades)
    book=load_workbook(grades)
    writer=pd.ExcelWriter(grades,engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    writer.write_cells()




list_files,grade_dic=readFiles()

write_summary(list_files)

