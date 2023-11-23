# import requests

# PROXY = requests.get("https://ipv4.webshare.io/",
#                 proxies={
#         "http": "http://xrrmhvbs-rotate:nxagk0sfe561@p.webshare.io:80/",
#         "https": "http://xrrmhvbs-rotate:nxagk0sfe561@p.webshare.io:80/"
#                 }).text
# print(PROXY)

# from datetime import date
# import pandas as pd
# TODAY = date.today()
# # NAME_OF_FILE = input("Enter name of the excel file: ")

# # df = pd.read_excel(NAME_OF_FILE)  # pip install openpyxl


# df = pd.read_csv("vo_cleanse.csv")
# df1 = df['Account Name'] + ', ' + df['Bill City'] + ', ' + df['Bill Zip']
# df1.to_csv(f"{TODAY}.csv", index=False)


# import pandas as pd 

# df = pd.read_csv('2023-10-05.csv')
# df1 = df[~df.company.str.contains('""')]
# df1.to_csv("hello.csv", index=False)