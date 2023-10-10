import gspread
import pandas as pd
from bs4 import BeautifulSoup
import bs4
from pylatexenc.latex2text import LatexNodes2Text
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import logging
import importlib
import cd
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig( filename='/home/binoy/second_answers/log_of_process.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def count_common_elements(list1, list2):
    list1_lower = [str(item).lower() for item in list1 if ~pd.isna(item)]
    list2_lower = [str(item).lower() for item in list2 if ~pd.isna(item)]
    common_elements = list(set(list1_lower).intersection(list2_lower))
    return len(common_elements)

def get_similarity_of_sentences(sen_1,sen_2):
    sentences = [sen_1,sen_2]
    sen_embeddings1 = model.encode(sentences)
    sim = cosine_similarity([sen_embeddings1[0]],[sen_embeddings1[1]])
    return round(sim[0][0],2)

def get_verdict(data):
    pass

def step_4():
    global model
    logging.info('STEP 4 process started...')
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    gc = gspread.service_account(filename = "/home/binoy/course-data-323207-5b61632e094e.json")
    google_sheet = gc.open('second_answers_final')

    comp_data_worksheet = google_sheet.worksheet('competitor_data')
    all_comp_data = comp_data_worksheet.get_all_records()
    comp_df = pd.DataFrame.from_dict(all_comp_data)
    ques_cols = [col for col in comp_df.columns if col.startswith('ques_html')]
    # opt_1_cols = [col for col in comp_df.columns if col.startswith('opt_1_html')]
    # opt_2_cols = [col for col in comp_df.columns if col.startswith('opt_2_html')]
    # opt_3_cols = [col for col in comp_df.columns if col.startswith('opt_3_html')]
    # opt_4_cols = [col for col in comp_df.columns if col.startswith('opt_4_html')]
    sol_cols = [col for col in comp_df.columns if col.startswith('sol_html')]
    if len(ques_cols) > 1:
        ques_cols.sort()
        comp_df['temp'] = ''
        for i in ques_cols:
            comp_df['temp'] = comp_df['temp'] + comp_df[i]
        comp_df.drop(columns=ques_cols,inplace = True)
        comp_df.rename(columns={'temp': 'ques_html'}, inplace=True)
    
    if len(sol_cols) > 1:
        sol_cols.sort()
        comp_df['temp'] = ''
        for i in sol_cols:
            comp_df['temp'] = comp_df['temp'] + comp_df[i]
        comp_df.drop(columns=sol_cols,inplace = True)
        comp_df.rename(columns={'temp': 'ques_html'}, inplace=True)

    cd_data_worksheet = google_sheet.worksheet('cd_data')
    all_cd_data = cd_data_worksheet.get_all_records()
    cd_df = pd.DataFrame.from_dict(all_cd_data)

    for i in comp_df.index:
        data = {}
        cd_id = comp_df['cd_id'][i]
        comp_url = comp_df['url'][i]
        domain = str(comp_df['domain'][i])
        module = importlib.import_module(domain)
        comp_ques = module.string_from_html(comp_df['ques_html'][i])
        comp_ans = module.string_from_html(comp_df['sol_html'][i])
        comp_options = [module.string_from_html(i).strip() for i in comp_df[['opt_1_html','opt_2_html','opt_3_html','opt_4_html']].iloc[i].tolist()]        
        math_check = [module.check_math_ques(i).strip() for i in comp_df[['ques_html','sol_html','opt_1_html','opt_2_html','opt_3_html','opt_4_html']].iloc[i].tolist()]

        temp = cd_df.loc[cd_df['cd_id'] == cd_id]
        cd_ques = cd.parse_cd_html(temp['question'].iloc[0])
        cd_ans = cd.parse_cd_html(temp['solution'].iloc[0])
        cd_options = [cd.parse_cd_html(temp['option1'].iloc[0]),cd.parse_cd_html(temp['option2'].iloc[0]),\
                    cd.parse_cd_html(temp['option3'].iloc[0]),cd.parse_cd_html(temp['option4'].iloc[0])]
        cd_url = temp['url'].iloc[0]

        ques_sim =  'NA'
        ans_sim =  'NA'
        common_options = count_common_elements(comp_options,cd_options)
        data['cd_id'] = cd_id
        data['comp_url'] = comp_url
        data['domain'] = domain
        data['cd_url'] = cd_url
        data['question_similarity'] = ques_sim
        data['answer_similarity'] = ans_sim
        data['common_options'] = common_options
        
        if common_options == 4:
            ques_sim =  get_similarity_of_sentences(comp_ques,cd_ques)
            ans_sim =  get_similarity_of_sentences(comp_ans,cd_ans)
            data['verdict'] = 'yes'
            google_sheet.values_append('similarity_data', {'valueInputOption': 'RAW'}, {'values': pd.DataFrame([data]).values.tolist()})
        elif 1 in math_check:
            data['verdict'] = 'no'
            data['reason'] = 'math content'
            google_sheet.values_append('rejected_content', {'valueInputOption': 'RAW'}, {'values': pd.DataFrame([data]).values.tolist()})
        else:
            ques_sim =  get_similarity_of_sentences(comp_ques,cd_ques)
            ans_sim =  get_similarity_of_sentences(comp_ans,cd_ans)
            if ques_sim > 0.9:
                data['verdict'] = 'yes'
            else:
                data['verdict'] = 'no'
            google_sheet.values_append('similarity_data', {'valueInputOption': 'RAW'}, {'values': pd.DataFrame([data]).values.tolist()})
