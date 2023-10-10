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
import time

def initiate_driver():
    PATH = "/usr/bin/chromedriver"
    service = Service(executable_path=PATH)
    options = Options()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('headless')
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-gpu')
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def logging_in(driver):
    url='https://quillbot.com/'
    driver.get(url)
    driver.find_element(By.XPATH,'//*[@id="root-client"]/div[2]/div[2]/div/header/div/div[3]/div/a/button').click()
    user_id = '/html/body/div[2]/div[2]/div[3]/section[1]/div/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/input'
    time.sleep(3)
    driver.find_element(By.XPATH,user_id).click()
    driver.find_element(By.XPATH,user_id).send_keys('rohini.mishra@collegedunia.com')
    time.sleep(2)
    passw= '/html/body/div[2]/div[2]/div[3]/section[1]/div/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]/div/input'
    login = '/html/body/div[2]/div[2]/div[3]/section[1]/div/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[5]/button'
    driver.find_element(By.XPATH,passw).click()
    driver.find_element(By.XPATH,passw).send_keys('Rm@123456')
    time.sleep(2)
    driver.find_element(By.XPATH,login).click()
    time.sleep(3)

def get_paraphrased_content(text):
    driver = initiate_driver()
    text_box = '/html/body/div[2]/div[2]/div[3]/section[1]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, text_box))).send_keys(text)
    button = '/html/body/div[2]/div[2]/div[3]/section[1]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/button'
    element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button)))
    element.click()
    output = '/html/body/div[2]/div[2]/div[3]/section[1]/div/div/div/div/div/div/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[1]'
    para_content = driver.find_element(By.XPATH,output).text
    return para_content

def logging_out(driver):
    profile = '/html/body/div[2]/div[2]/div[2]/div/header/div/div[3]/div/div/span/button'
    profile_ele = driver.find_element(By.XPATH,profile)
    logout = '/html/body/div[8]/div[3]/div/div[2]'
    a = ActionChains(driver)
    a.move_to_element(profile_ele).perform()
    time.sleep(2)
    driver.find_element(By.XPATH,logout).click()

driver.quit()
driver.refresh()