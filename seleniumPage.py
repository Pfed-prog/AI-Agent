import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
options = Options()
#options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

driver.get("https://d-id-talks-prod.s3.us-west-2.amazonaws.com/google-oauth2%7C110628693356570030047/tlk_GLoidR-pZwomUwO2hoSO2/1769869443779.mp4?AWSAccessKeyId=AKIA5CUMPJBIK65W6FGA&Expires=1769955847&Signature=GvfYu5YTxcY%2FU5lx5IAHlWRgblE%3D")

wait = WebDriverWait(driver, 10)  
element = wait.until(EC.presence_of_element_located((By.ID, "example")))