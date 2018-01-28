from tkinter import *
import nltk
import pandas as pd
import collections
import os

def browse():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename
def update_gradebook():
    os.chdir('C:\\Users\\E-Neo.DESKTOP-M4A5E83\\workspace\\textanalysis\\bin')
    os.system('java KahootScorer')
def write_summary(grade_dic):
    list_files=['Pre Test','Post Test']
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

        for assignment in range(0,len(grade_dic[student])):
            stuff.write(str(grade_dic[student][assignment]) + ',')
            total += grade_dic[student][assignment]
        if(total==2):
            stuff.write('1.0' + ',')
        elif(total==1):
            stuff.write('0.25'+',')
        elif(total==0):
            stuff.write('0.0'+',')
        stuff.write(str(float(total / total_points) * 100) + '%' + ',')

    stuff.close()

print('Pick Gradebook')
grades=browse()
print('Pick Pre Test to add')
toAdd=browse()
print('Pick Post Test')
post=browse()


gradebook=pd.read_csv(grades)
pre_test=pd.read_csv(toAdd)
post_test=pd.read_csv(post)

dic=collections.defaultdict(lambda : [0,0])
for student in range(0,len(gradebook['SIS Login ID'])-1):
    dic[gradebook['SIS Login ID'][student]]=[0,0]

for student in range (0,len(pre_test['Email Address'])):
    dic[pre_test['Email Address'][student]][0]=1

for student in range (0,len(post_test['Email Address'])):
    dic[post_test['Email Address'][student]][1]=1

write_summary(dic)












