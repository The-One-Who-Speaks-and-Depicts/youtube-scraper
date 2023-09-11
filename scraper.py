import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from selenium.webdriver import FirefoxOptions
from selenium import webdriver

import argparse
import os

from tqdm import tqdm

import json

class Example:

    def __init__(self, text, intent, entities):
        self.text = text
        self.intent = intent
        self.entities = entities
        
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, ensure_ascii=False).encode('utf8')

def main(args):
    data=[]
    
    options = FirefoxOptions()
    options.add_argument('--headless')

    with webdriver.Firefox(options=options) as driver:
        wait = WebDriverWait(driver,15)
        driver.get(args.link)

        for item in tqdm(range(200)): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(15)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
            if comment.text:
                data.append(comment.text)
            
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    with open(os.path.join(data_path, args.name + ".json"), "a", encoding="utf-8") as outfile:    
        for i in data:
            outfile.write(Example(i, "", []).toJSON().decode()) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--link', '-l', help='Link to the youtube video')
    parser.add_argument('--name', '-n', help='Name of the file to save comments')
    args = parser.parse_args()
    main(args)