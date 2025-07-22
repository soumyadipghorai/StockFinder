import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os 
import logging
from tqdm import tqdm 
import streamlit as st
from datetime import datetime

download_dir = r"C:\Users\ghora\Downloads" 
with open("data/all_company.json", "r") as json_file:
    all_company = json.load(json_file)  
    
def download_file():
    service = Service(executable_path='chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Open browser maximized
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")  # Add a User-Agent
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    

    driver = webdriver.Chrome(service=service, options= chrome_options)

    url = "https://www.nseindia.com/report-detail/eq_security" 
    driver.get(url)

    time.sleep(2)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    for company in tqdm(all_company) :
        try :
            input_field = wait.until(EC.visibility_of_element_located((By.ID, "hsa-symbol")))
            input_field.send_keys(Keys.CONTROL + 'a') 
            input_field.send_keys(Keys.DELETE)
            
            time.sleep(0.5)
            input_field.send_keys(company)

            dropdown_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tt-suggestion.tt-selectable")))
            dropdown_option.click()

            one_year_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "oneY"))
            )

            one_year_button.click()

            download_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@download='equity-derivatives.csv']"))
            )
            download_button.click()
            time.sleep(5)

            today = datetime.today()
            day_today = today.day
            month_today = today.month
            year_today = today.year

            file_name = f"{day_today}-{month_today}-{year_today-1}-TO-{day_today}-{month_today}-{year_today}-{company}-ALL-N.csv"  # File to be moved

            destination_folder =  "./dump"
            destination_path = os.path.join(destination_folder, file_name)

            source_path = os.path.join(download_dir, file_name)
            
            try: 
                if os.path.exists(source_path): 
                    shutil.move(source_path, destination_path)
                    logging.info(f"File moved to: {destination_path}")
                else:
                    logging.info("File not found in Downloads folder.")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

        except Exception as e : 
            st.error(e)
            
        time.sleep(2)
        

    return True 