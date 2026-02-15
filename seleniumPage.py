import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

options = Options()
#options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

url = "https://d-id-talks-prod.s3.us-west-2.amazonaws.com/google-oauth2%7C111801002690343760251/tlk_lTHMxqrnmxNI4Q1O1dwSw/1770123088735.mp4?AWSAccessKeyId=AKIA5CUMPJBIK65W6FGA&Expires=1770209496&Signature=A44OkmXCuX9RxTRmfrXbyPzbxLc%3D"

driver.get(url)

time.sleep(10)

driver.close()