from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
import numpy as np
import warnings
import os
import time
import json
from datetime import datetime
warnings.filterwarnings('ignore')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

df = pd.read_csv("Urls.csv")
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import emoji  # Import the emoji library

options = Options()
options.add_argument("--mute-audio")
options.headless = True
DRIVER_PATH = "chromedriver.exe"
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
from selenium.common.exceptions import TimeoutException


from PIL import Image
import io
import re

def remove_emojis(text):
    # Regular expression pattern to match emojis
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "]+"
    )
    return emoji_pattern.sub('', text)

def extract_reviews(soup):
    # Extract the reviews from the current page's BeautifulSoup object (soup)
    reviews = soup.find("div", class_="common-reviews__list").find_all("div", class_="j-expose__common-reviews__list-item")
    return reviews

# Flag variable to check if the reviews have been sorted or not
reviews_sorted = False

def get_reviews(url, max_pages=None):
    
    global reviews_sorted
    
    driver.get(url)
    
    # Sort reviews only if they have not been sorted before
    if not reviews_sorted:
        # Locate the "Most Recent to Oldest" option and click on it to sort the reviews
        most_recent_to_oldest_option = driver.find_element(By.CLASS_NAME, 'common-reviews__select-box-list').find_elements(By.TAG_NAME,"li")[0]
        driver.execute_script("arguments[0].click();", most_recent_to_oldest_option)

        # Wait for a moment (1 second) for the reviews to be sorted
        time.sleep(10)
        reviews_sorted = True

    all_reviews = []
    page_count = 0

    while max_pages is None or page_count <= max_pages:
        #reviews_container = driver.find_element(By.CLASS_NAME, 'common-reviews__list')
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        reviews_on_page = extract_reviews(soup)
        all_reviews.extend(reviews_on_page)

        try:
            next_button = driver.find_element(By.XPATH, '//span[@class="sui-pagination__next sui-pagination__btn sui-pagination__hover"]')
            is_next_button_disabled = next_button.get_attribute("disabled")
            if is_next_button_disabled:
                break
            else:
                driver.execute_script("arguments[0].click();", next_button)
        except NoSuchElementException:
            break

        page_count += 1

    driver.quit()

    # Adjust the number of reviews to return based on max_pages
    if max_pages is not None:
        return all_reviews[3:max_pages * 3+3]
    else:
        return all_reviews
    

def scrap_product(link,max_pages):
    ##################################################################################
    reviews_list = get_reviews(link,max_pages)

    ###########################################################################################################################
    
##############################################################################################################################    
    # Create an empty list to store the data
    data = []
    for i, review in enumerate(reviews_list):

        size_and_weight = review.find('div', class_="gd-detail")
        if size_and_weight is not None:
            size_and_weight = size_and_weight.findAll("div",class_="gd-detail-item")

        if len(size_and_weight)==2  :
            try:
                bust_size = size_and_weight[0].text.split(":")[1].strip()
            except AttributeError:
                bust_size = ''

            try:
                weight = size_and_weight[1].text.split(":")[1].strip()
            except AttributeError:
                weight = ''
        else:
            bust_size = ''
            weight = ''

        try:
            rating = review.find('div', class_='rate-star')["aria-label"].replace("Rating","")
        except AttributeError:
            rating = ''
            
        try:
            review_date = review.find('div', class_='date').text
        except AttributeError:
            review_date = ''

        comment_tag_box = review.find('div', class_='comment-tag-box')
        rate_des = review.find('div', class_='rate-des')

        if comment_tag_box and comment_tag_box.text.strip():
            review_text = comment_tag_box.text.strip()
        elif rate_des and rate_des.text.strip():
            review_text = rate_des.text.strip()
        else:
            review_text = "No review text found"

        all_fits_info = review.find('div', class_='rate-fit').findAll("span",class_="rate-fit__item")
        if all_fits_info is not None:
            if len(all_fits_info)==3:
                try:
                    overall_fit = all_fits_info[0].text.split(":")[1].strip()
                except AttributeError:
                    overall_fit = ''

                try:
                    fit_color = all_fits_info[1].text.split(":")[1].strip()
                except AttributeError:
                    fit_color = ''

                try:
                    fit_size = all_fits_info[2].text.split(":")[1].strip()
                except AttributeError:
                    fit_size = ''
            else:
                overall_fit = ''
                fit_color = ''
                fit_size = ''
        else:
            overall_fit = ''
            fit_color = ''
            fit_size = ''
        
        review_text = remove_emojis(review_text)
        

        review_data = {
            'id': i+1,
            'weight': weight,
            'bust': bust_size,
            'star': rating,
            'review': review_text,
            'overall fit': overall_fit,
            'color': fit_color,
            'size': fit_size,
            'review_date': review_date
        }
        data.append(review_data)

    json_data = json.dumps(data, indent=4,ensure_ascii=False)
    json_data = json.loads(json_data)

    ###########################################################################################################################
    return json_data

df["reviews"] = np.nan
df = df.astype(str)

# loop over the rows of the DataFrame, scrape each link, and add the new features to the DataFrame
for index, row in df[:10].iterrows():
    print(index)
    link = row['sku_url']
    #link = "https://us.shein.com/Ruffle-Trim-Push-Up-Bikini-Swimsuit-p-18268887-cat-1866.html?src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_3%60ps%3D4_3%60jc%3Dreal_2039&src_module=Women&src_tab_page_id=page_home1682698249374&mallCode=1"
    print(link)
    # Connection
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    
    sku_sub_cat = row["sub_category"]
    
    #json_data = scrap_product(link,max_pages=20)
    json_data = scrap_product(link,max_pages=2)


    df.at[index, "reviews"] = json_data


df.to_csv("Data.csv",encoding="utf-8")