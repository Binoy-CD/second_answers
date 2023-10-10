from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import gspread
import image_part
import bd_unlocker_api
import bs4
import csv
import json
import logging
import traceback
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig( filename='/home/binoy/second_answers/log_of_process.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def toppr_url_scraper(id,url,domain):
    data = {}
    data['id'] = id
    data['domain'] = domain
    data['url'] = url
    try:
        html_string = bd_unlocker_api.get_html(url)
        soup = BeautifulSoup(html_string,'html.parser')
        time.sleep(10)
        data['ques_html'] = soup.find("div", attrs={"class": "TopprQuestion_questionBody__OBlTc"})
        options_dict = {}
        options = soup.find_all("div", attrs={"class": "options_answr"})
        for i in range(len(options)):
            options_dict['opt_%d_html'%(i+1)] = options[i]
        data['sol_html'] = soup.find("h2", attrs={"class": "Solution_html__KkUW2"})
        data.update(options_dict)
        logging.info('Succesfully fetched the data from toppr...')
    except Exception as ex:
        tb = traceback.extract_tb(ex.__traceback__)
        filename, lineno, func, line = tb[-1]
        logging.info(f"---------Error occurred in File: {filename}, Line: {lineno}, Function: {func}")
        logging.info(f"---------Line of code with error: {line}")
        logging.info('Error in fetching data from toppr...')
        return pd.DataFrame(columns = cols)
    return data

def replace_equations_with_placeholders(sentence):
    placeholders = {}
    count = 1

    def repl(match):
        nonlocal count
        equation = match.group()
        if equation not in placeholders:
            placeholders[equation] = f" x_{count} "
            count += 1
        return placeholders[equation]

    pattern = r'\\\(.*?\\\)|\\\[.*?\\\]'
    replaced_sentence = re.sub(pattern, repl, sentence)

    return replaced_sentence, placeholders

def toppr_html_parser(answer_html):
    sentence = ''
    img_count = 0
    img_data = {}
    for child in answer_html.descendants:
        if isinstance(child,bs4.element.Tag):
            if isinstance(child,bs4.element.Tag):
                if child.name == 'img':
                    temp_dict = image_part.cleaning_image_part(child,img_count)
                    img_data.update(temp_dict)
                    sentence+= 'y_%d'%img_count
            if child.name == 'katex':
                return 0,0
        if isinstance(child, bs4.element.NavigableString):
            sentence+= ' '+child+' '
    sentence = sentence.replace('$', ' $ ')
    updated_sentence = re.sub(r'\s+', ' ', sentence)
    prepared_text = updated_sentence
    return prepared_text,img_data

    # sentence = ''
    # img_count = 0
    # img_data = {}
    # for child in answer_html.descendants:
    #     if isinstance(child,bs4.element.Tag):
    #         if child.name == 'img':
    #             temp_dict = image_part.cleaning_image_part(child,img_count)
    #             img_data.update(temp_dict)
    #             sentence+= 'y_%d'%img_count
    #     if isinstance(child, bs4.element.NavigableString):
    #         sentence+= ' '+child+' '
    # sentence = sentence.replace('$', ' $ ')
    # updated_sentence = re.sub(r'\s+', ' ', sentence)
    # prepared_text,eqn_placeholders = replace_equations_with_placeholders(updated_sentence)
    # return prepared_text,img_data,eqn_placeholders

def string_from_html(html_string):
    final_text = ''
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.NavigableString):
            final_text= final_text+child+' '
    final_text = re.sub(r'\s+', ' ', final_text)
    final_text = final_text.replace('\xa0',' ')
    return final_text

def check_math_ques(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.Tag):
            if 'class' in child.attrs:
                if 'katex' in child.attrs['class']:
                    return 1
    return 0

def check_image(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.Tag):
            if child.name == 'img':
                return 1
    return 0
