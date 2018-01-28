from tkinter import *
import pandas as pd
import collections

def browse():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename

print('Pick survey')
survey=browse()
print('pick answer key')
answers=browse()

survey_data=pd.read_csv(survey)
answer_data=pd.read_csv(answers)

def calc_score(row):
    score=0
    for i in range(1,10):
        print('Q' + str(i) + '   ' + str(survey_data['Q' + str(i)][row]) + '  ' + str(answer_data['Q' + str(i)][0])+str(str(survey_data['Q'+str(i)][row])==str(answer_data['Q'+str(i)][0])))
        if (str(survey_data['Q'+str(i)][row])==str(answer_data['Q'+str(i)][0])):
            score+=1
    return score

dic=collections.defaultdict(lambda :0)
for index in range(0,len(survey_data['ID'])):
    no=0
    if(survey_data['Finished'][index]==True or survey_data['Finished'][index]=='TRUE' and survey_data['ID'][index] not in dic.keys() ):
        dic[survey_data['ID'][index]]=calc_score(index)
    elif (survey_data['ID'][index] in dic.keys()):
        tempscore=calc_score(index)
        if(tempscore>dic[survey_data['ID'][index]]):
            dic[survey_data['ID'][index]] = calc_score(index)
            print('Happened'+str(no))
            no+=1




df=pd.DataFrame.from_dict(dic,orient='index')

df.to_csv('PreTest Scores.csv')


