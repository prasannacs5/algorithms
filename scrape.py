from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import traceback

def load_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")  # Mimic a real user-agent

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

def load_url(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
        return None
    
file_path = '/Users/prasanna.selvaraj/Downloads/macys_url1.csv'

def scrape_df(df):
    for index, row in df.iterrows():
        url = row['site_url']
        print(url,"\n")
        try:
            driver = load_driver()
            driver.get(url)
            #time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.find_all('span', class_='price-lg')  # Replace with actual class/ID
            for product in products:
                print(product.get_text(strip=True))

            desc = soup.find_all('div', class_='long-description medium')  # Replace with actual class/ID
            for des in desc:
                print(des.get_text(strip=True))
        except Exception as e:
            print(f"Unexpected error with URL {url}: {e}")
            traceback.print_exc()
    driver.quit()

def split_dataframe(df, num_splits):
    batch_size = len(df) // num_splits
    for i in range(num_splits):
        yield df.iloc[i * batch_size: (i + 1) * batch_size]

df = load_url(file_path)
# Iterate through each smaller DataFrame
for i, small_df in enumerate(split_dataframe(df, 100)):
    scrape_df(small_df)


