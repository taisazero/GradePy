from tkinter import *
import pandas as pd
import collections

def browse():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename

print('Pick CSV ')
csv=browse()

csv_data=pd.read_csv(csv)
def compare_columns (column1,column2):
    list1=[]
    list2=[]
    diff1=[]
    diff2=[]
    for row in range(0,len(csv_data[column1])) :
        cell=csv_data[column1][row]
        list1.append(cell)
    for row in range(0, len(csv_data[column2])):
        cell=csv_data[column2][row]
        list2.append(cell)

    for data in list1:
        if(data not in list2):
            diff1.append(data)
    for data in list2:
        if(data not in list1 and data not in diff1):
            diff2.append(data)

    return diff1,diff2

list1,list2=compare_columns('Gradebook','pretest')
df=pd.DataFrame({'list 1':list1,'list 2':list2})
df.to_csv('difference.csv')
print ('list 1',list1)
print('list 2',list2)