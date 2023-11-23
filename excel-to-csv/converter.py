from datetime import date
import pandas as pd
TODAY = date.today()
NAME_OF_FILE = input("Enter name of the excel file: ")

df = pd.read_excel(NAME_OF_FILE)  # pip install openpyxl
df1 = df['Company Name'] + ', ' + df['Location']
df1.to_csv(f"{TODAY}.csv", index=False)