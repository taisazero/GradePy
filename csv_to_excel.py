import glob, os
import pandas as pd

from pandas import DataFrame, ExcelWriter


writer = ExcelWriter(r"C:\Users\E-Neo.DESKTOP-M4A5E83\Desktop\.xlsx")
file = pd.ExcelFile()

for filename in glob.glob(r"C:\Users\E-Neo.DESKTOP-M4A5E83\Downloads\Lab Reflection Topics-20180815T123242Z-001\Lab Reflection Topics\NMF\*.csv"):
    df_csv = pd.read_csv(filename)

    (_, f_name) = os.path.split(filename)
    (f_short_name, _) = os.path.splitext(f_name)

    df_csv.to_excel(writer, f_short_name, index=False)
    print(f_name+' done')
writer.save()