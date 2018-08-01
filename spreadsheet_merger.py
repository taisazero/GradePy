from tkinter import *
import pandas as pd
import collections
from tkinter.filedialog import askdirectory

def browse():
    root = Tk()
    root.withdraw()
    filename = askdirectory()
    return filename


final_dic=collections.defaultdict(lambda :[])
print('enter directory csv ')
dir=browse()
csv=input('enter primary filename: ')

csv=pd.read_csv(dir+'\\'+csv)
num=input('how many csvs to merge?')
keyz=input('primary key: ')

for key in csv.keys():
    for row in range(0,len(csv[key])):
        final_dic[key].append(csv[key][row])
for i in range(1,int(num)):
    print('Pick csv ')
    csv_2 = csv=input('enter filename: ')
    csv_2 = pd.read_csv(dir+'\\'+csv_2)
    key_2 = input('matching key: ')
    for main_row in range(0, len(final_dic[keyz])):
        for row in range(0, len(csv_2[key_2])):
            if final_dic[keyz][main_row]==csv_2[key_2][row]:
                for temp_key in csv_2.keys():
                    if temp_key!=key_2:
                        final_dic[temp_key+'('+str(i)+')'][main_row]=csv_2[temp_key][row]

pd.DataFrame(final_dic).to_csv('result.csv')
