from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from login import login_and_save_cookies
import os
import pickle
import time
import tempfile
import base64
import os

def restore_cookies_from_env(env_var="B64_COOKIES", target_path="fb_cookies.pkl"):
    b64_data = os.environ.get(env_var)
    if not b64_data:
        raise Exception(f"❌ Environment variable {env_var} not set")
    
    # Remove any cert headers/footers if present (from certutil)
    b64_cleaned = ''.join(line for line in b64_data.splitlines() if "CERTIFICATE" not in line)
    
    with open(target_path, "wb") as f:
        f.write(base64.b64decode(b64_cleaned))
    print("✅ fb_cookies.pkl restored from environment variable")

def load_cookies(driver, cookies_file):
    restore_cookies_from_env()
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
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless=new")  # ✅ Good for CircleCI or CI/CD environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Use a unique temp directory to avoid user-data-dir conflict
    temp_user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_user_data_dir}")

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
        tweet_box.click()
        tweet_box.send_keys(tweet)
        print(f"Tweet to post:\n{tweet}")

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