from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv()

# Function to initialize the driver.
def init_driver():
    options = webdriver.ChromeOptions()
    # Add any necessary options here. For example: options.add_argument('--headless') for headless mode.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Optional login function.
def login(driver, url, username_selector, username, password_selector, password, submit_button_selector):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        # Enter username.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, username_selector))).send_keys(username)

        # Enter password.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, password_selector))).send_keys(password)

        # Click the submit button to log in.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector))).click()

        # Wait until some element that signifies we are logged in is present on page. Adjust as needed!
        logged_in_element = 'SOME_ELEMENT_INDICATING_SUCCESS'
        
        if wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, logged_in_element))):
            print("Logged in successfully.")
            return True
        
    except Exception as e:
         print(f"An error occurred during login: {e}")
    
    return False

# Function to accept cookies if cookie banner is present.
def accept_cookies(driver):
    try:
       cookie_banner_accept_button_locator = (By.XPATH,'//button[contains(text(), "Accept")]')  # Update this xpath according to your needs.

       WebDriverWait(driver ,10).until(
           EC.visibility_of_element_located(cookie_banner_accept_button_locator)).click()
       
       print("Accepted cookies.")
    
    except Exception as e:
         print(f"No cookie banner found or error clicking it: {e}")

# Main execution area where you can structure your scraping tasks using above functions 
if __name__ == "__main__":
    
     # Initialize the web driver
     driver = init_driver()

     try:
         url_to_scrape = 'https://example.com'  # Replace with your target URL.

         accept_cookies(driver)  # Accept cookies if the banner is there.

         success_login = login(
             driver,
             url=url_to_scrape,
             username_selector='#username',   # Replace with correct selector or id for username field element. 
             username='your_username',      # Replace with real credentials or pass them securely through environment variables or other means!
             password_selector='#password',   # Replace with correct selector or id for password field element. 
             password='your_password',      # As above use real credentials securely!
             submit_button_selector='#submit'   # Replace with correct selector or id of the login button element. 
         )

         if success_login:
            pass  ## Put additional logic here after successful authentication.

         
     finally:
          ## Do any cleanup like closing browser etc here..
          driver.quit()

