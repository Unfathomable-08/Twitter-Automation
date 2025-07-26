from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from login import login_and_save_cookies
import os
import pickle
import time

def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("Cookies loaded.")
    else:
        raise Exception("❌ Cookies file not found. Run login script first.")

def post_on_twitter(tweet):
    # Init driver
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)

    try:
        # Load Twitter and inject cookies
        driver.get("https://x.com/")
        driver.delete_all_cookies()
        load_cookies(driver, "fb_cookies.pkl")

        # Open post page
        driver.get("https://x.com/compose/post")
        print("Post Modal Opened")

        # Wait for the tweet textarea to load
        time.sleep(10)
        tweet_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
        )

        # Tweet
        tweet_box.send_keys(tweet)

        # Click Post btn
        post_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, '[data-testid="tweetButton"]'
            ))
        )
        post_button.click()

    except Exception as e:
        print(f"Error posting tweet: {e}")
    finally:
        driver.quit()