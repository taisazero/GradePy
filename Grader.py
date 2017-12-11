from tkinter import *
import nltk
import pandas as pd

def browse():
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename

print('Pick Gradebook')
grades=browse()
print('Pick grades to add')
toAdd=browse()

gradebook=pd.read_csv(grades)
new_grades=pd.read_csv(toAdd)




