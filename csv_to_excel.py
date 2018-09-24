import glob, os
import pandas as pd

from pandas import DataFrame, ExcelWriter


writer = ExcelWriter(r"pair_ngrams_unfiltered.xlsx")
#file = pd.ExcelFile(writer)

for filename in glob.glob(r"C:\Users\Zero\Documents\cohesionScripts\Lab Reflection Topics\collective\*.csv"):
    df_csv = pd.read_csv(filename)

    (_, f_name) = os.path.split(filename)
    (f_short_name, _) = os.path.splitext(f_name)

    df_csv.to_excel(writer, f_short_name, index=False)
    print(f_name+' done')

writer.save()
writer.close()