import os
import time
import multiprocessing

import pandas as pd

from extractor import main_scrape


def starter():
    """CLI visible to the end-user"""
    os.system('cls')
    print("-------------------------------------------")
    print("""         Google Maps Scraper           """)
    print("-------------------------------------------")

    name_of_file = input("Enter the name of the csv file in the io folder: ")
    # current_directory = os.getcwd()
    io_folder = 'io_folder'
    os.chdir(io_folder)
    new_directory = os.getcwd()
    print(f'You are currently in the right path: {new_directory}')

    print("Please wait...")
    os.system('cls')

    # Reads the csv file
    df = pd.read_csv(name_of_file)
    print('Processing the file....')
    df1 = df.iloc[:, 0]
    keywords = df1.to_list()
    keyword_length = len(keywords)
    # print(f'These are the keywords: {keywords}')
    print(f"Read all the {keyword_length} keywords in the csv file...")

    print("The result will be saved in --> 'file.csv' in the io_folder")
    print("The Scraping starting in..")
    for number in range(3, 0, -1):
        print(number)
        time.sleep(1)
    os.system('cls')

    # multiprocessing code
    num_processes = 15
    pool = multiprocessing.Pool(num_processes)
    try:
        # # applying function to each keyword
        pool.map(main_scrape, keywords)
    except Exception as err_mp:
        with open("logs.txt", "a", encoding='UTF-8') as f:
            f.write(str(err_mp))
    # Close the pool
    pool.close()
    pool.join()


if __name__ == "__main__":
    starter()
