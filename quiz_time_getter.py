from urllib import request as request
from urllib import parse as parser
from urllib import
from bs4 import BeautifulSoup
import urllib3
from requests.auth import HTTPDigestAuth
import requests

url='https://uncc.instructure.com/courses/54437/gradebook/speed_grader?assignment_id=209052#%7B%22student_id%22%3A%2268165%22%7D'

responsez = requests.get(url,auth=HTTPDigestAuth('ealhossa','Taisa!zero000'))



print(responsez.text)


