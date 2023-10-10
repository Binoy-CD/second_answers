import gspread
import pandas as pd
import ast
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def initiate_driver():
    logging.info('Initiating driver...')
    global driver
    PATH = "/usr/bin/chromedriver"
    py = "127.0.0.1:24001"
    # service = Service(executable_path=PATH)
    options = Options()
    options.add_argument('--proxy-server=%s' % py)
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('headless')
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-gpu')
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(PATH, options=options)
    return driver

def upload_on_qacms(cd_id,content,image_details,driver):
    driver.get('https://qacms.collegedunia.com/test/questions')
    driver.find_element(By.XPATH,'//*[@id="phrase"]').send_keys(cd_id)
    driver.find_element(By.XPATH,'//*[@id="root"]/section/section/main/div[1]/div/form/div[2]/div/div/div[2]/button').click()
    time.sleep(5)
    ques_in_table_ele = driver.find_element(By.XPATH,'//tr[@data-row-key="%s"]'%cd_id)
    ques_in_table_ele.find_element(By.XPATH,'./td[2]/span/button').click()
    other_sol_ele = driver.find_element(By.XPATH,'//form[@class="ant-form ant-form-vertical question-form"]/div[12]')
    
    driver.execute_script("arguments[0].scrollIntoView();", other_sol_ele)
    other_sol_ele.find_element(By.XPATH,'.//button').click()
    time.sleep(5)

    other_sol_ele.find_element(By.XPATH,'.//input[@value="EDITOR"]').click()
    time.sleep(2)

    other_sol_ele.find_element(By.XPATH,'.//div[@role="textbox"]').send_keys(content)
    
    if len(image_details)>0:
        other_sol_ele.find_element(By.XPATH,'.//input[@value="HTML"]').click()
        before_image_content = other_sol_ele.find_element(By.XPATH,'.//textarea[@id="otherSolutions_0_text_en"]').text
        for i in image_details.keys():
            after_image_content = before_image_content.replace('y_%s'%str(i),image_details[i])
        other_sol_ele.find_element(By.XPATH,'.//textarea[@id="otherSolutions_0_text_en"]').send_keys(after_image_content)
    
    time.sleep(5)
    driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div/div[2]/form/div[16]/div[1]/div[1]/button').click()

def step_6():
    gc = gspread.service_account(filename = "/home/binoy/course-data-323207-5b61632e094e.json")
    google_sheet = gc.open('second_answers_final')

    para_data_worksheet = google_sheet.worksheet('paraphrased_content')
    para_data = para_data_worksheet.get_all_records()
    para_df = pd.DataFrame.from_dict(para_data)

    cd_data_worksheet = google_sheet.worksheet('cd_data')
    all_cd_data = cd_data_worksheet.get_all_records()
    cd_df = pd.DataFrame.from_dict(all_cd_data)

    for i in para_df.index:
        driver = initiate_driver()
        cd_id = para_df['cd_id']
        cd_url = cd_df[cd_df['cd_id'] == cd_id]['url'].iloc[0]
        image_details = para_df['image_details'][i]
        content = para_df['uploading_content'][i]
        
        if pd.isna(image_details):
            images_list = []
        else:
            images_list= ast.literal_eval(image_details)
        
        upload_on_qacms(cd_id,content,images_list,driver)
