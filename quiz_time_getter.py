import pandas as pd
import requests

from canvasapi import Canvas
from canvasapi.requester import Requester
from canvasapi.submission import Submission
from canvasapi.group import Group
import ast
import re
import collections
import statistics


# Canvas API URL
API_URL = "https://uncc.instructure.com/"
# Canvas API key
file=open('token.txt','r')

API_KEY = str(file.read())
file.close()
# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course_id=int(input('enter course id: '))
quiz_id= int(input('enter quiz id: '))
course=canvas.get_course(course_id)


print('Extracting from: '+course.name)
quiz=course.get_quiz(quiz_id)
quiz_json=quiz.to_json()





r=requests.get("https://uncc.instructure.com/api/v1/courses/"+str(course_id)+"/quizzes/"+str(quiz_id)+"/submissions/?per_page=100",headers={'Authorization': 'Bearer '+API_KEY})
quiz_submissions=r.json()['quiz_submissions']
print('# Submissions: '+str(len(quiz_submissions)))
output={}
group_dict=collections.defaultdict(lambda :[])
for submission in quiz_submissions:
    user_id=submission['user_id']
    user=ast.literal_eval(course.get_user(submission['user_id']).to_json())
    groups= course.get_groups()
    student_name = user['name']
    group_name='No Group'
    total_points = float(re.findall(r'\"points_possible\": [0-9.]+',quiz_json)[0].split(':')[1].strip())
    if submission['kept_score']!=None:
        score=float(submission['kept_score'])/total_points*100
    else:
        score=0
        print(student_name+' no submission')
    for group in groups:
        for member in group.get_users():
            if ast.literal_eval(member.to_json())['id']==user_id:
                group_name=str(group)
                group_name=re.findall(r' [A-Z] ',group_name)[0].strip()
    group_dict[group_name].append(student_name)

    if submission['time_spent']!=None:
        time_spent=float(submission['time_spent']/60.0)
    else:
        time_spent=None
    output[student_name]={'time':time_spent,'group':group_name,'score':score}

act_name=str(re.findall(r'\"title\": \"[A-Z :.a-z0-9(),\-]+\"',quiz_json)[0].split(':')[1].strip())
act_name=act_name.replace(' ','')
act_name=act_name.replace('\"','')
act_name=act_name.lower()
print('results: '+str(output))
df=pd.DataFrame.from_dict(output,orient='index')
file_name=act_name+'_results.csv'
df.to_csv(file_name)
print('Processing Groups...')
group_results={}
print(group_dict)
for group in group_dict.keys():
    time_list=[]
    score_list=[]
    for student in group_dict[group]:
        if output[student]['time']!=None:
            time_list.append(output[student]['time'])
        score_list.append(output[student]['score'])
    if len(score_list)>=2 and len(time_list)>=2:
        time_mean=statistics.mean(time_list)
        time_std_dev=statistics.stdev(time_list)
        score_mean = statistics.mean(score_list)
        score_std_dev = statistics.stdev(score_list)
        score_median=statistics.median(score_list)
    else:
        time_mean=time_list[0]
        time_std_dev=0
        score_mean=score_list[0]
        score_std_dev=0
        score_median=score_list[0]
    group_results[group]={'time mean':time_mean, 'time standard dev':time_std_dev,'score mean': score_mean,'score standard deviation':score_std_dev,'score median':score_median}

print('results: '+str(group_results))
df=pd.DataFrame.from_dict(group_results,orient='index')
file_name=act_name+'_results_group_analysis.csv'
df.to_csv(file_name)



