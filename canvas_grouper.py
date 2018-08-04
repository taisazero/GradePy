import pandas as pd
import collections
from canvasapi import Canvas
from nltk.metrics import edit_distance as ed
import re
from tkinter import Tk
# Canvas API URL
def browse_file():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename
class Grouper:
    def __init__(self,course_id):
        self.course_id=course_id

    def get_group_dic(self):
        group_dic=collections.OrderedDict()
        API_URL = "https://uncc.instructure.com/"
        # Canvas API key
        file=open('token.txt','r')

        API_KEY = str(file.read())
        file.close()
        # Initialize a new Canvas object
        canvas = Canvas(API_URL, API_KEY)
        course=canvas.get_course(self.course_id)
        print('Extracting Groups from: '+course.name)
        groups= course.get_groups()
        for group in groups:
            if 'table' in group.name.lower() and 'group' in group.name.lower():
                group_name=group.name.replace(' ','')
                group_name = re.findall(r'GroupID:[A-Z]+', group_name)[0].split(':')[1].strip()
                group_dic[str(group_name)] = []
                for user in group.get_users():
                    group_dic[str(group_name)].append({'id': int(user.id), 'name': str(user.name)})


            elif 'table' in group.name.lower():
               group_dic[str(group.name)]=[]
               for user in group.get_users():
                   group_dic[str(group.name)].append({'id':int(user.id),'name':str(user.name)})

        print(
            'Due to Canvas API BS restrictions we need to ask for the student logins file. Please Browse and select the student logins csv file.' +
            ' It needs to have the following columns : Student, ID, Login')

        logins_file = browse_file()
        df = pd.read_csv(logins_file, index_col=1)
        for group in group_dic.keys():
            for student_index in range(0, len(group_dic[group])):
                temp = group_dic[group][student_index]
                student = {'id': temp['id'], 'name': temp['name'], 'login': df.loc[temp['id']]['Login']}
                group_dic[group][student_index] = student

        return group_dic


