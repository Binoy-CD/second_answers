from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import bd_unlocker_api
import csv
import logging
import image_part
import bs4
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig( filename='/home/binoy/second_answers/log_of_process.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def vedantu_scraper(id,url,domain):
    question_data=[]
    try:
        html_string = bd_unlocker_api.get_html(url)
        soup = BeautifulSoup(html_string,'html.parser')

        # Scrape the question and options data
        results = soup.find_all("div", class_="Question_questionWrapper__5XheM")
        for result in results:
            ques_text = result.find(id="question-section-id").text.split('?')[0].replace('"', '').strip()
            Options_text_1 = result.find(id="question-section-id").text.split('?')[-1].replace('"', '').strip()
            ques_html = str(soup.find(id="question-section-id"))

        Qoption_text = Options_text_1

        # Split each element after the dot (".")
        split_options = Qoption_text.split('(')[1:]

        # Assign each element to corresponding variables
        opt_1 = split_options[0]
        opt_1_html = str(soup.find(id="question-section-id"))
        opt_2 = split_options[1]
        opt_2_html = str(soup.find(id="question-section-id"))
        opt_3 = split_options[2]
        opt_3_html = str(soup.find(id="question-section-id"))
        opt_4 = split_options[3]
        opt_4_html = str(soup.find(id="question-section-id"))

        ques_html = str(soup.find(id="question-section-id"))

        # Scrape the solution data
        solutions = soup.find("div", class_="Answer_description__TYtWw")
        sol=[]
        for i in solutions:
           sol.append(i.text.split('Complete')[-1].replace('"', '').strip())
        text_without_quotes = [t.replace('"', '') for t in sol[4:]]
        sol=[]
        for line in text_without_quotes:
           sol.append(line)

        sol_html = str(soup.find(id="answer-section-id"))

        question_data.append((id, url, domain, ques_text, ques_html, opt_1, opt_1_html, opt_2, opt_2_html, opt_3, opt_3_html, opt_4, opt_4_html, sol, sol_html))
    except Exception as e:
        print(str(e)+' in first try')
        pass

    try:
        html_string = bd_unlocker_api.get_html(url)
        soup = BeautifulSoup(html_string,'html.parser')

        # Scrape the question and options data
        results = soup.find_all("div", class_="Question_questionWrapper__5XheM")
        for result in results:
            ques_text = result.find(id="question-section-id").text.split('A')[0].replace('"', '').strip()
            Options_text_2 = result.find(id="question-section-id").text.split('A')[-1].replace('"', '').strip()
    
        Qoption_text = Options_text_2

        # Split each element after the dot (".")
        split_options = Qoption_text.split('. ')[1:]

        # Assign each element to corresponding variables
        opt_1 = split_options[0]
        opt_1_html = str(soup.find(id="question-section-id"))
        opt_2 = split_options[1]
        opt_2_html = str(soup.find(id="question-section-id"))
        opt_3 = split_options[2]
        opt_3_html = str(soup.find(id="question-section-id"))
        opt_4 = split_options[3]
        opt_4_html = str(soup.find(id="question-section-id"))

        ques_html = str(soup.find(id="question-section-id"))
        # Scrape the solution data
        solutions = soup.find("div", class_="Answer_description__TYtWw")
        sol=[]
        for i in solutions:
           sol.append(i.text.split('Complete')[-1].replace('"', '').strip())
        text_without_quotes = [t.replace('"', '') for t in sol[4:]]
        sol=[]
        for line in text_without_quotes:
           sol.append(line)

        sol_html = str(soup.find(id="answer-section-id"))

        question_data.append((id, url, domain, ques_text, ques_html, opt_1, opt_1_html, opt_2, opt_2_html, opt_3, opt_3_html, opt_4, opt_4_html, sol, sol_html))
    except Exception as e:
        print(str(e)+' in second try')
        pass
    
    try:
        html_string = bd_unlocker_api.get_html(url)
        soup = BeautifulSoup(html_string,'html.parser')

        # Scrape the question and options data
        results = soup.find_all("div", class_="Question_questionWrapper__5XheM")
        for result in results:
            ques_text = result.find(id="question-section-id").text.split('(a')[0].replace('"', '').strip()
            Options_text_3 = result.find(id="question-section-id").text.split('(a')[-1].replace('"', '').strip()
            ques_html = str(soup.find(id="question-section-id"))

        Qoption_text = Options_text_3

        # Split each element after the dot (".")
        split_options = Qoption_text.split(')')[1:]

        # Assign each element to corresponding variables
        opt_1 = split_options[0]
        opt_1_html = str(soup.find(id="question-section-id"))
        opt_2 = split_options[1]
        opt_2_html = str(soup.find(id="question-section-id"))
        opt_3 = split_options[2]
        opt_3_html = str(soup.find(id="question-section-id"))
        opt_4 = split_options[3]
        opt_4_html = str(soup.find(id="question-section-id"))

        ques_html = str(soup.find(id="question-section-id"))

        # Scrape the solution data
        solutions = soup.find("div", class_="Answer_description__TYtWw")
        sol=[]
        for i in solutions:
           sol.append(i.text.split('Complete')[-1].replace('"', '').strip())
        text_without_quotes = [t.replace('"', '') for t in sol[4:]]
        sol=[]
        for line in text_without_quotes:
           sol.append(line)

        sol_html = str(soup.find(id="answer-section-id"))

        question_data.append((id, url, domain, ques_text, ques_html, opt_1, opt_1_html, opt_2, opt_2_html, opt_3, opt_3_html, opt_4, opt_4_html, sol, sol_html))
    except Exception as e:
        print(str(e)+' in third try')
        pass
    df_output = pd.DataFrame(question_data, columns=['id', 'url', 'domain', 'ques_text', 'ques_html', 'opt_1', 'opt_1_html', 'opt_2', 'opt_2_html', 'opt_3', 'opt_3_html', 'opt_4', 'opt_4_html', 'sol', 'sol_html'])
    logging.info('driver closed and fetched the competitor data')
    return df_output

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

    pattern = r'\$.*?\$|\\\[.*?\\\]'
    replaced_sentence = re.sub(pattern, repl, sentence)

    return replaced_sentence, placeholders

def vedantu_html_parser(answer_html):
    sentence = ''
    img_count = 0
    img_data = {}
    for child in answer_html.descendants:
        if isinstance(child,bs4.element.Tag):
            if child.name == 'img':
                temp_dict = image_part.cleaning_image_part(child,img_count)
                img_data.update(temp_dict)
                sentence+= 'y_%d'%img_count
        if isinstance(child, bs4.element.NavigableString):
            sentence+= ' '+child+' '
    sentence = sentence.replace('$', ' $ ')
    updated_sentence = re.sub(r'\s+', ' ', sentence)
    prepared_text,eqn_placeholders = replace_equations_with_placeholders(updated_sentence)
    return prepared_text,img_data,eqn_placeholders

def string_from_html(html_string):
    final_text = ''
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.NavigableString):
            final_text= final_text+child+' '
    final_text = re.sub(r'\s+', ' ', final_text)
    final_text = final_text.replace('\xa0',' ')
    return final_text

def check_image(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.Tag):
            if child.name == 'img':
                return 1
    return 0
