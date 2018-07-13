from tkinter import *
import pandas as pd
import collections
import statistics

def browse():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename

print('Pick CSV ')
csv=browse()

csv_data=pd.read_csv(csv)
group_column= input('Enter the group column: ')

menu=input('1. one column \n2. multiple columns: ')
if menu ==1:
    analysis=input('Enter the analysis column: ')

    temp_dic=collections.defaultdict(lambda :[])
    for row in range(0,len(csv_data[group_column])) :
        temp_dic[csv_data[group_column][row]].append(float(csv_data[analysis][row]))
    final_dic={}
    for key in temp_dic.keys():
        print(temp_dic[key])
        if key!='A':
            final_dic[key]=[statistics.mean(temp_dic[key]),statistics.stdev(temp_dic[key])]
        else:
            final_dic[key] = [27.5,0 ]
    df=pd.DataFrame(final_dic)
    df.to_csv('aggregated.csv')
else:
    num=input('How many columns?')

    analysis=[]
    temp_dic = collections.defaultdict(lambda: [])
    final_dic = collections.defaultdict(lambda: [])
    for i in range(0,int(num)):
        analysis.append(input('Enter the analysis column: '))

    for column in analysis:
        temp_dic = collections.defaultdict(lambda: [])
        for row in range(0, len(csv_data[group_column])):
            if csv_data[group_column][row] != 'LOL' and csv_data[group_column][row] != 'A':
                temp_dic[csv_data[group_column][row]].append(float(csv_data[column][row]))
        for row in range(0, len(csv_data[group_column])):
            if csv_data[group_column][row] != 'LOL' and csv_data[group_column][row] != 'A':
                for row in range(0, len(csv_data[group_column])):
                    if csv_data[group_column][row] == 'LOL':
                        total= csv_data[column][row]
                        break
        for group in temp_dic.keys():
                if group != 'LOL' and group != 'A':
                    final_dic[group].append(float(statistics.mean(temp_dic[group] )/total )*100)


    print(final_dic)
    to_print={}
    for key in final_dic.keys():
        print(final_dic[key])
        if key != 'A':
            to_print[key] = [statistics.mean(final_dic[key]), statistics.stdev(final_dic[key])]

    df = pd.DataFrame(to_print)
    df.to_csv('aggregated.csv')



