from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")
print("Page title is:", driver.title)

time.sleep(3)
driver.quit()