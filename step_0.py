import pandas as pd
import gspread
import re
import ast
import logging
import warnings
import cd
warnings.filterwarnings("ignore")

logging.basicConfig( filename='/home/binoy/second_answers/log_of_process.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def getting_cd_id(text):
    pattern = '"(.*)"'
    return re.findall(pattern, text)[0]

def get_options(text):
    if pd.isna(text):
        return 0
    options_data = {}
    options_list= ast.literal_eval(text)
    for i in range(len(options_list)):
        options_data['option%d'%(i+1)] = options_list[i]['en']
    return options_data

def step_0():
    logging.info('STEP 0 process started...')
    gc = gspread.service_account(filename = "/home/binoy/course-data-323207-5b61632e094e.json")
    google_sheet = gc.open('second_answers_final')
    cd_id_worksheet = google_sheet.worksheet('cd_id_for_upload')
    cd_id_data = cd_id_worksheet.get_all_records()
    cd_id_df = pd.DataFrame.from_dict(cd_id_data)

    all_questions = pd.read_csv('/home/binoy/second_answers/questions.csv',index_col=False)
    all_questions['id'] = all_questions['_id'].apply(getting_cd_id)

    final_columns = ['id','option1','option2','option3','option4','option5','question','solution','url']
    final_df = pd.DataFrame(columns = final_columns)
    
    for i in cd_id_df.index:
        data = {}
        for col in final_columns:
            data[col] = 'NA'
        cd_id = cd_id_df['cd_id'][i]
        data['id'] = cd_id
        temp = all_questions.loc[all_questions['id'] == cd_id]
        if len(temp) < 1:
            logging.info(f"Couldn't fetch the details for the id : {cd_id}. since id details not found in the csv...")
            continue
        options = get_options(temp['options'].iloc[0])
        if options !=0:
            data.update(options)
        data['question'] = temp['text.en'].iloc[0]
        data['solution'] = temp['solution.text.en'].iloc[0]
        data['url'] = 'https://collegedunia.com/exams/questions/'+str(temp['slugPrefix'].iloc[0])+'-'+str(temp['id'].iloc[0])
        data['question_type'] = temp['Type'].iloc[0]
        
        img_check = cd.check_image_question(data['question'])
        if img_check == 1:
            google_sheet.values_append('img_questions', {'valueInputOption': 'RAW'}, {'values': pd.DataFrame([data]).values.tolist()})
            continue

        # check_1 = cd.check_cd_math_ques(data['question'])
        # check_2 = cd.check_cd_math_ques(data['solution'])
        # if check_1 == 0 or check_2 ==0:
        #     math_df = pd.concat([final_df,pd.DataFrame([data])],ignore_index=True)
        #     google_sheet.values_append('math_questions', {'valueInputOption': 'RAW'}, {'values': math_df.values.tolist()})
        #     logging.info("Found questions with mathematical content, so ignoring those questions and updating them in another sheet...")
        #     continue
        final_df = pd.concat([final_df,pd.DataFrame([data])],ignore_index=True)

    google_sheet.values_append('cd_data', {'valueInputOption': 'RAW'}, {'values': final_df.values.tolist()})
    logging.info("Fetched the cd data details from the csv for the given cd ids and updated in the google sheet...")
