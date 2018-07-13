from tkinter import *
import pandas as pd
import collections
import re



def browse():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename

print('Pick Student Key File ')
key_file=browse()

key_file=pd.read_csv(key_file)

print('Pick file you want to de-identify')
file=browse()

filex=open(file,'r')
csv_file=filex.read()
filex.close()


for row in range(0,len(key_file['id'])):
    print(key_file['id'][row]+' '+str(int(key_file['d-id'][row])))
    csv_file=csv_file.replace(str(key_file['id'][row]),str(int(key_file['d-id'][row])))


final_file=open(file,'w')
final_file.write(csv_file)
final_file.close()


