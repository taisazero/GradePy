import pandas as pd
from tkinter import Tk
import os
import collections
from canvasapi import Canvas
from canvasapi.requester import Requester
from canvasapi.submission import Submission
from canvasapi.group import Group
from pandas import ExcelWriter
from pandas import ExcelFile
from nltk.metrics import edit_distance as ed
from canvas_grouper import Grouper
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import Tk

def browse_file():
    Tk().withdraw()
    filename = askopenfilename(title='Choose the student logins file')
    return filename


def browse_dir():
    Tk().withdraw()
    name=askdirectory()
    return name


print('Select Directory: ')
dir=browse_dir()
semester=input('Input Semester: ')

p=os.path.abspath(os.curdir)
if os.path.exists(p+'\\kahoot_reports')==False:
    os.makedirs(p+'\\kahoot_reports')

if os.path.exists(p+'\\kahoot_reports\\'+str(semester))==False:
    os.makedirs(p+'\\kahoot_reports\\'+str(semester))



grouper=Grouper(int(input('Enter course ID: ')))

group_dic=grouper.get_group_dic()



#group_dic = sorted(group_dic.items(), key=lambda x: x[0])



for root, dirs, files in os.walk(dir):
    for file in files:
        df=pd.read_excel(file)


