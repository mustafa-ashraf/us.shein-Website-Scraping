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

options = Options()
options.add_argument("--mute-audio")
options.headless = True
DRIVER_PATH = "chromedriver.exe"
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
from selenium.common.exceptions import TimeoutException


from PIL import Image
import io
import time

def scrap_product(link,sub_category):
    ##################################################################################
    try:
            driver.get(link)
#             time.sleep(10)
            wait = WebDriverWait(driver, 10)
            section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-intro')))
            info = section.find_element(By.CLASS_NAME, 'product-intro__info')

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            ##################################################################################
            sku_name = None
            try:
                sku_name_elem = info.find_element(By.CLASS_NAME, "product-intro__head-name")
                if sku_name_elem:
                    sku_name = sku_name_elem.text.strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            sku_id = None
            try:
                sku_id_elem = info.find_element(By.CLASS_NAME, "product-intro__head-sku")
                if sku_id_elem:
                    sku_id = sku_id_elem.text.split(":")[1].strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            price = None
            try:
                price_element = info.find_elements(By.CLASS_NAME, "original")
                if len(price_element)>0:
                    price = price_element[0].text.strip()
                else:
                    price_element = info.find_element(By.CLASS_NAME, "discount")
                    if price_element is not None:
                        price = price_element.text.strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            club_price = None
            try:
                club_price_div = info.find_element(By.CLASS_NAME, "paidvip__content")
                if club_price_div is not None:
                    club_price_info = club_price_div.find_element(By.CLASS_NAME, "paidvip__info")
                    if club_price_info is not None:
                        club_price = club_price_info.find_element(By.TAG_NAME, "div").text.strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            orig_price = None
            try:
                orig_price_elem = info.find_elements(By.CLASS_NAME, "del-price")
                if len(orig_price_elem)>0:
                    orig_price = orig_price_elem[0].text.strip()
                else:
                    orig_price_elem = info.find_element(By.CLASS_NAME, "original")
                    if orig_price_elem is not None:
                        orig_price = orig_price_elem.text.strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            badge = None
            try:
                badge_elem = info.find_element(By.CLASS_NAME, "product-intro__head-label")
                if badge_elem:
                    badge = badge_elem.text
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            size = None
            try:
                size_element = soup.find("div",class_="product-intro__size-choose")
                if size_element:
                    sizes = size_element.findAll("span")
                    size = ";".join([size.text for size in sizes]).replace(" ","")
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            quick_ship = None
            try:
                quick_ship_element = info.find_element(By.CLASS_NAME, "goodsd-sizes__quickship")
                if quick_ship_element is not None:
                    quick_ship = quick_ship_element.text.replace("\n","")
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            delivery_1 = None
            try:
                freeshipping = info.find_element(By.CLASS_NAME, "product-intro__freeshipping")
                if freeshipping:
                    freeshipping_abt = freeshipping.find_element(By.CLASS_NAME, "product-intro__freeshipping-abt")
                    if freeshipping_abt:
                        active_slide = freeshipping_abt.find_element(By.CLASS_NAME, "swiper-slide-active")
                        if active_slide:
                            delivery_1 = active_slide.text.replace("\n"," ")
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            delivery_2 = None
            try:
                freeshipping = info.find_element(By.CLASS_NAME, "product-intro__freeshipping")
                if freeshipping:
                    freeshipping_abt = freeshipping.find_element(By.CLASS_NAME, "product-intro__freeshipping-abt")
                    if freeshipping_abt:
                        active_slide = freeshipping_abt.find_element(By.CLASS_NAME, "swiper-slide-next")
                        if active_slide:
                            delivery_2 = active_slide.text.replace("\n"," ")
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            return_policy = None
            try:
                return_policy = soup.findAll("div",class_="modal-dialog")[4].text.split(":")[1].replace("\xa0","").replace("\n","").split("Learn More")[0]
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            descrption = None
            try:
                #soup = BeautifulSoup(driver.page_source, 'html.parser')
                descriptions = soup.find("div",class_="product-intro__description-table").findAll("div",class_="product-intro__description-table-item")
                descrption = ""
                for i in descriptions:
                    descrption = descrption + str(i.find("div",class_="key").text) + str(i.find("div",class_="val").text)+";"
            except (AttributeError, IndexError, NoSuchElementException):
                pass
            ###############################################################################
            model_size = None
            size_div = soup.find("div", class_="product-intro__sizeguide-summary-list")
            if size_div:
                size_divs = size_div.findAll("div")
                if size_divs and len(size_divs) > 0:
                    try:
                        model_size = size_divs[0].text.split(":")[1].strip()
                    except (IndexError, NoSuchElementException):
                        pass
            ##################################################################################
            model_height = None
            height_div = soup.find("div", class_="product-intro__sizeguide-summary-list")
            if height_div:
                height_divs = height_div.findAll("div")
                if height_divs and len(height_divs) > 2:
                    try:
                        model_height = height_divs[2].text.split(":")[1].strip()
                    except (IndexError, NoSuchElementException):
                        pass
            ##################################################################################
            # For model_Bust
            model_Bust = None
            try:
                model_Bust_div = soup.find("div", class_="product-intro__sizeguide-summary-list")
                if model_Bust_div is not None:
                    model_Bust = model_Bust_div.findAll("div")[3].text.split(":")[1].strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            # For model_waist
            model_waist = None
            try:
                model_waist_div = soup.find("div", class_="product-intro__sizeguide-summary-list")
                if model_waist_div is not None:
                    model_waist = model_waist_div.findAll("div")[4].text.split(":")[1].strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            # For model_hips
            model_hips = None
            try:
                model_hips_div = soup.find("div", class_="product-intro__sizeguide-summary-list")
                if model_hips_div is not None:
                    model_hips = model_hips_div.findAll("div")[5].text.split(":")[1].strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            brand = None
            try:
                brand = soup.find("div",class_='product-intro__brand-title')
                if brand is not None:
                    brand = brand.text.strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            collection = None
            try:
                collection = soup.find("div",class_="product-intro__brand-des")
                if collection is not None:
                    collection = collection.text.strip()
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            avg_rating = None
            try:
                # Wait up to 10 seconds for the element to be present
                avg_rating_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "rate-num"))
                )
                if avg_rating_element is not None:
                    avg_rating = avg_rating_element.text.strip()
            except (TimeoutError, NoSuchElementException):
                pass
            ##################################################################################
            rating_num = None
            try:
                # Wait up to 10 seconds for the element to be present
                rating_num_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "product-intro__head-reviews"))
                )
                if rating_num_element is not None:
                    rating_num = rating_num_element.text
            except (TimeoutError, NoSuchElementException):
                pass
            ####################################################################################
            fits = None
            try:
                # Wait up to 10 seconds for the elements to be present
                fits = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "fit-item"))
                )
            except (TimeoutError, NoSuchElementException):
                pass
            ##################################################################################
            fit_small = None
            try:
                if fits and len(fits) > 0:
                    fit_small = fits[0].text
            except (IndexError, NoSuchElementException):
                pass  
            ###################################################################################
            fit_true = None
            try:
                if fits and len(fits) > 1:
                    fit_true = fits[1].text
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################
            fit_large = None
            try:
                if fits and len(fits) > 2:
                    fit_large = fits[2].text
            except (IndexError, NoSuchElementException):
                pass    
            ##################################################################################
            img_url = None
            try:
                #x = soup.find("div", class_="swiper-container").find("img")
                x = soup.find("div", class_="swiper-slide-active").find("img")
                if x is not None and "data-src" in x.attrs:
                    img_url = "https:" + str(x["data-src"])
                elif x is not None and "src" in x.attrs:
                    img_url = "https:" + str(x["src"])
            except (AttributeError, IndexError, KeyError, NoSuchElementException):
                pass
            
#             print("-----------: ",img_url)
            ##################################################################################
            time_stamp = None
            try:
                timestamp = int(time.time())
                time_stamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            except (IndexError, NoSuchElementException):
                pass
            ##################################################################################    

            # create women folder if it doesn't exist
            if not os.path.exists("women"):
                os.mkdir("women")

            # create category folder if it doesn't exist
            category_folder_path = os.path.join("women", sub_category)
            if not os.path.exists(category_folder_path):
                os.mkdir(category_folder_path)

            # create product folder
            product_folder_path = os.path.join(category_folder_path, sku_id)
            if not os.path.exists(product_folder_path):
                os.mkdir(product_folder_path)

            # Download images

            images_code = soup.find("div",class_='product-intro__galleryWrap').find("div",class_="swiper-wrapper").findAll("div",class_='swiper-slide')
            #print("-------------",img_url)
            response = requests.get(img_url)  
            # Open the image using Pillow
            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')
            img.save(os.path.join(product_folder_path, "{}.jpg".format("0")), 'JPEG', quality=10)
            
            if images_code:
                images_code = images_code[1:]
                for i, image in enumerate(images_code):
                    if image.find("img",class_="j-verlok-lazy"):
                        the_image_url = "https:" + image.find("img",class_="j-verlok-lazy")["data-src"]
                        #print(the_image_url)
                    else:
                        continue
                    response = requests.get(the_image_url)
                    # Open the image using Pillow
                    img = Image.open(io.BytesIO(response.content))
                    img = img.convert('RGB')

                    # Compress the image using JPEG format and save it
                    img.save(os.path.join(product_folder_path, "{}.jpg".format(i)), 'JPEG', quality=10)
                
           
                
                    
    except Exception as e:
        # handle other exceptions
        return (None,) * 26
    ###########################################################################################################################
    return sku_name,sku_id,price,club_price,orig_price,badge,size,quick_ship,delivery_1,delivery_2,return_policy,descrption,model_size,model_height,model_Bust,model_waist,model_hips,brand,collection,avg_rating,rating_num,fit_small,fit_true,fit_large,img_url,time_stamp


# add columns for the features
df['sku_name'] = np.nan
df['sku_id'] = np.nan
df['price'] = np.nan
df['club_price'] = np.nan
df['orig_price'] = np.nan
df['badge'] = np.nan
df['size'] = np.nan
df['quick_ship'] = np.nan
df['delivery_1'] = np.nan
df['delivery_2'] = np.nan
df['return_policy'] = np.nan
df['descrption'] = np.nan
df['model_size'] = np.nan
df['model_height'] = np.nan
df['model_Bust'] = np.nan
df['model_waist'] = np.nan
df['model_hips'] = np.nan
df['brand'] = np.nan
df['collection'] = np.nan
df['avg_rating'] = np.nan
df['rating_num'] = np.nan
df['fit_small'] = np.nan
df['fit_true'] = np.nan
df['fit_large'] = np.nan
df['img_url'] = np.nan
df['time_stamp'] = np.nan


# loop over the rows of the DataFrame, scrape each link, and add the new features to the DataFrame
for index, row in df[:10].iterrows():
    print(index)
    link = row['sku_url']
    print(link)
    sku_sub_cat = row["sub_category"]
    
    sku_name,sku_id,price,club_price,orig_price,badge,size,quick_ship,delivery_1,delivery_2,return_policy,descrption,model_size,model_height,model_Bust,model_waist,model_hips,brand,collection,avg_rating,rating_num,fit_small,fit_true,fit_large,img_url,time_stamp = scrap_product(link,sku_sub_cat)
    # add the new features to the DataFrame
    df.at[index, 'sku_name'] = sku_name
    df.at[index, 'sku_id'] = sku_id
    df.at[index, 'price'] = price
    df.at[index, 'club_price'] = club_price
    df.at[index, 'orig_price'] = orig_price
    df.at[index, 'badge'] = badge
    df.at[index, 'size'] = size
    df.at[index, 'quick_ship'] = quick_ship
    df.at[index, 'delivery_1'] = delivery_1
    df.at[index, 'delivery_2'] = delivery_2
    df.at[index, 'return_policy'] = return_policy
    df.at[index, 'descrption'] = descrption
    df.at[index, 'model_size'] = model_size
    df.at[index, 'model_height'] = model_height
    df.at[index, 'model_Bust'] = model_Bust
    df.at[index, 'model_waist'] = model_waist
    df.at[index, 'model_hips'] = model_hips
    df.at[index, 'brand'] = brand
    df.at[index, 'collection'] = collection
    df.at[index, 'avg_rating'] = avg_rating
    df.at[index, 'rating_num'] = rating_num
    df.at[index, 'fit_small'] = fit_small
    df.at[index, 'fit_true'] = fit_true
    df.at[index, 'fit_large'] = fit_large
    df.at[index, 'img_url'] = img_url
    df.at[index, 'time_stamp'] = time_stamp
  
# Count the number of NaN values in each row
nan_counts = df.isnull().sum(axis=1)

# Filter rows with less than 26 NaN values
filtered_df = df[nan_counts < 26]

filtered_df.to_csv("test2.csv",index=False)