from selenium import webdriver
import pickle

def login_and_save_cookies():
    driver = webdriver.Chrome()
    driver.get("https://x.com/")
    
    input("Log in manually, then press Enter here...")

    # Save cookies after successful login
    with open("fb_cookies.pkl", "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    
    print("Cookies saved.")
    driver.quit()

if __name__ == "__main__":
    login_and_save_cookies()