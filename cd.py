from pylatexenc.latex2text import LatexNodes2Text
from bs4 import BeautifulSoup
import bs4
import warnings
warnings.filterwarnings("ignore")

def get_text_from_cd_html(html):
    final_text = ''
    math_content = []
    soup = BeautifulSoup(html, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.Tag):
            if 'class' in child.attrs:
                if 'math-tex' in child.attrs['class']:
                    for i in child.strings:
                        math_content.append(i)
                        plain_text = LatexNodes2Text().latex_to_text(i)
                        final_text+= plain_text
        elif isinstance(child, bs4.element.NavigableString) and child not in math_content:
            final_text+=child
    return final_text.replace('\xa0',' ')

def parse_cd_html(html_string):
    final_text = ''
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.NavigableString):
            final_text= final_text+child+' '
    final_text = final_text.replace('\xa0',' ')
    return final_text

def check_cd_math_ques(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.Tag):
            if 'class' in child.attrs:
                if 'math-tex' in child.attrs['class']:
                    return 0
    return 1

def check_image_question(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    for child in soup.descendants:
        if isinstance(child,bs4.element.Tag):
            if child.name == 'img':
                return 1
    return 0
