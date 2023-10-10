import pandas as pd
import gspread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from gspread_dataframe import set_with_dataframe
import sys
import time
import vedantu
import byjus
import toppr
import embibe
import traceback
import logging
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig( filename='/home/binoy/second_answers/log_of_process.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def step_3():
    logging.info('STEP 3 process started...')
    final_columns = ['cd_id','url','domain','ques_html','opt_1_html','opt_2_html','opt_3_html','opt_4_html','sol_html']

    gc = gspread.service_account(filename = "/home/binoy/course-data-323207-5b61632e094e.json")
    google_sheet = gc.open('second_answers_final')

    google_serp_worksheet = google_sheet.worksheet('google_serp_data')
    all_serp_data = google_serp_worksheet.get_all_records()
    serp_df = pd.DataFrame.from_dict(all_serp_data)

    comp_data_worksheet = google_sheet.worksheet('competitor_data')
    all_comp_data = comp_data_worksheet.get_all_records()
    comp_df = pd.DataFrame.from_dict(all_comp_data)

    df = serp_df[['url','cd_id','domain']]
    df.drop_duplicates(inplace=True)
    logging.info('Dropped duplicate data from the competitor urls data...')

    for i in df.index:
        comp_dict = {}
        comp_df = pd.DataFrame(columns = final_columns)
        url = df['url'][i]
        cd_id = df['cd_id'][i]
        domain = df['domain'][i]
        print(url)
        try:
            if domain == 'vedantu':
                logging.info('Calling the vedantu scraper...')
                comp_dict = vedantu.vedantu_scraper(cd_id,url,'vedantu')
            elif domain == 'toppr':
                logging.info('Calling the toppr scraper...')
                comp_dict = toppr.toppr_url_scraper(cd_id,url,'toppr')
            elif domain == 'embibe':
                logging.info('Calling the embibe scraper...')
                comp_dict = embibe.embibe_scraper(cd_id,url,'embibe')
            elif domain == 'byjus':
                logging.info('Calling the byjus scraper...')
                comp_dict = byjus.byjus_scraper(cd_id,url,'byjus')
            # elif domain == 'askfilo':
            #     comp_df = askfilo(cd_id,url)
            if comp_dict == 0:
                continue
            final_data = {}
            for key in comp_dict.keys():
                comp_dict[key] = str(comp_dict[key])
                content = comp_dict[key]
                if len(content) > 50000:
                    for limit in range(0,int(len(content)/50000)+1):
                        if limit == 0:
                            final_data[key] = content[limit*49999:(limit+1)*49999]
                        else:
                            final_data[key+"_"+str(limit)] = content[limit*49999:(limit+1)*49999]
                else:
                    final_data[key] = content
            
            comp_df = pd.concat([comp_df,pd.DataFrame([final_data])],ignore_index = True)
            comp_df = comp_df.fillna('NA')
            comp_data_worksheet.clear()
            set_with_dataframe(worksheet=comp_data_worksheet, dataframe=comp_df, include_index=False,include_column_header=True, resize=True)
            # google_sheet.values_append('competitor_data', {'valueInputOption': 'RAW'}, {'values': comp_df.values.tolist()})
            logging.info(f'Fetched data from {domain}... and updated the data in google sheet...')
        except Exception as ex:
            tb = traceback.extract_tb(ex.__traceback__)
            filename, lineno, func, line = tb[-1]
            logging.info(f"---------Error occurred in File: {filename}, Line: {lineno}, Function: {func}")
            logging.info(f"---------Line of code with error: {line}")
            error_df = df.iloc[[i]]
            error_df['error'] = str(ex)
            google_sheet.values_append('competitor_data_failed', {'valueInputOption': 'RAW'}, {'values': error_df.values.tolist()})
        finally:
            time.sleep(5)
