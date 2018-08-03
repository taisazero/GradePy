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


def browse_file():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename
def browse_dir():
    from tkinter.filedialog import askdirectory
    Tk().withdraw()
    name=askdirectory()
    return name


print('Select Directory: ')
dir=browse_dir()
semester=input('Input Semester')

group_dic=collections.OrderedDict()

for root, dirs, files in os.walk(dir):
    for file in files:
        f=open(file,'r')
        pd.read_excel()

