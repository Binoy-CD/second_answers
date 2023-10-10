import gspread
import pandas as pd
from bs4 import BeautifulSoup
import logging
import warnings
import cd
warnings.filterwarnings("ignore")
logging.basicConfig( filename='/home/binoy/second_answers/log_of_process.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def search_text(text):
    words = text.split(' ')
    count = len(words)
    batches = []
    queries = []
    for i in range(0,int(count/32)+1):
        if i == int(count/32):
            batches.append(words[-32:])
            continue
        batches.append(words[i*32:(i+1)*32])
    for i in batches:
        string = ' '.join([str(elem) for elem in i])
        queries.append(string)
    return queries

def step_1():
    logging.info('STEP 1 process started...')
    gc = gspread.service_account(filename = "/home/binoy/course-data-323207-5b61632e094e.json")
    google_sheet = gc.open('second_answers_final')

    cd_data_worksheet = google_sheet.worksheet('cd_data')
    all_questions_data = cd_data_worksheet.get_all_records()
    questions_df = pd.DataFrame.from_dict(all_questions_data)

    final_df = pd.DataFrame(columns = ['cd_id','parsed_question','search_queries'])
    for i in questions_df.index:
        data = {}
        data['parsed_question'] = cd.get_text_from_cd_html(questions_df['question'][i])
        data['search_queries'] = search_text(data['parsed_question'])
        temp = pd.DataFrame(data)
        temp['cd_id'] = questions_df['cd_id'][i]

        final_df = pd.concat([temp,final_df],ignore_index=True)

    google_sheet.values_append('search_queries', {'valueInputOption': 'RAW'}, {'values': final_df.values.tolist()})
    logging.info('Search queries for google search prepared and updated in the google sheet...')
