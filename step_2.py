import pandas as pd
import gspread
import ssl
import urllib.request
import urllib.parse
import tldextract
import json
import logging
import traceback
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig( filename='/home/binoy/second_answers/log_of_process.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def get_site_specific_serp(search_query,cd_id):
    try:
        # sites = ' site:toppr.com'
        sites = ' site:askfilo.com OR site:byjus.com OR site:embibe.com OR site:toppr.com OR site:vedantu.com' #OR site:doubtnut.com
        temp= pd.DataFrame()
        ssl._create_default_https_context = ssl._create_unverified_context
        query = urllib.parse.quote(search_query+sites).replace('/','%2F')
        opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {'http': 'http://brd-customer-hl_a4a3b5b0-zone-questions_serp:bdmzmy3683ha@zproxy.lum-superproxy.io:22225',
            'https': 'http://brd-customer-hl_a4a3b5b0-zone-questions_serp:bdmzmy3683ha@zproxy.lum-superproxy.io:22225'}))
        response = opener.open('https://www.google.com/search?q='+query+'&hl=en&num=50&lum_json=1')
        google_search = response.read().decode('utf-8')
        google_search_json = json.loads(google_search)
        data = google_search_json
        
        if google_search_json['general']['results_cnt'] == 0:
            logging.info(f'Got zero search result fot the keyword {search_query}.')
            return 'zero_results'

        if "organic" in data.keys():
            temp = pd.concat([temp,pd.DataFrame(data['organic'])],ignore_index=True)
        if "featured_snippets" in data.keys():
            temp = pd.concat([temp,pd.DataFrame(data['featured_snippets'])],ignore_index=True)
            
        temp1 = temp[['rank', 'link', 'description', 'title', 'display_link', 'global_rank']]
        temp1['domain'] = temp1['link'].apply(lambda row: tldextract.extract(row).domain)
        temp1['keyword'] = search_query
        temp1['cd_id'] = cd_id
        domain_url = {'embibe':'embibe.com/questions/','toppr':'toppr.com/ask/question/',\
                      'byjus':'byjus.com/question-answer/','vedantu':'vedantu.com/question-answer/'}
        relevant_df = pd.DataFrame()
        for i in domain_url.keys():
            temp2 = temp1[temp1['domain'] == i]
            temp2 = temp2[temp2['link'].str.contains(domain_url[i], case=False)]
            relevant_df = pd.concat([temp2,relevant_df],ignore_index =True)
        sorted_df = relevant_df.sort_values(by='rank', ascending=True)
        google_sheet.values_append('google_serp_data', {'valueInputOption': 'RAW'}, {'values': sorted_df.values.tolist()})
        return 1
    except Exception as ex:
        tb = traceback.extract_tb(ex.__traceback__)
        filename, lineno, func, line = tb[-1]
        logging.info(f"---------Error occurred in File: {filename}, Line: {lineno}, Function: {func}")
        logging.info(f"---------Line of code with error: {line}")
        return str(ex)

def step_2():
    logging.info('STEP 2 process started...')
    gc = gspread.service_account(filename = "/home/binoy/course-data-323207-5b61632e094e.json")
    global google_sheet
    google_sheet = gc.open('second_answers_final')

    search_queries_worksheet = google_sheet.worksheet('search_queries')
    all_search_queries_data = search_queries_worksheet.get_all_records()
    search_queries_df = pd.DataFrame.from_dict(all_search_queries_data)

    for i in search_queries_df.index:
        value = get_site_specific_serp(search_queries_df['search_query'][i],search_queries_df['cd_id'][i])
        temp = search_queries_df[['search_query','cd_id']].iloc[[i]]
        if value !=1:
            temp['status'] = value
            google_sheet.values_append('google_serp_error', {'valueInputOption': 'RAW'}, {'values': temp.values.tolist()})
            logging.info('Failed to fetch google serp results and updated the same in the google sheet...')
