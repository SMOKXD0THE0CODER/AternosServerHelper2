import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import subprocess

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def start_minecraft_server():
    try:
        logging.info("Killing any existing Chrome or ChromeDriver processes.")
        subprocess.call("TASKKILL /f /IM CHROME.EXE", shell=True)
        subprocess.call("TASKKILL /f /IM CHROMEDRIVER.EXE", shell=True)

        # Define ChromeOptions
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "--user-data-dir=C:/Users/smokx/AppData/Local/Google/Chrome/User Data")  # Adjust the path to your user data directory
        chrome_options.add_argument("--profile-directory=Profile 1")  # Adjust to the profile directory name you need

        # Initialize the WebDriver with the defined options
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open the Minecraft hosting page
        driver.get('https://aternos.org/server/')

        # Log in to the hosting account
        wait = WebDriverWait(driver, 10)
        skip_ad = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="rNbtrDfNtcXK"]/div/div[2]/div[3]/div[2]/div[1]')))
        skip_ad.click()
        start_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="start"]')))
        start_button.click()

        yield 'Сервер запускается...'

        # Continuously check for changes in response
        while True:
            time.sleep(10)

            # Get the current response
            current_response = driver.find_element(By.XPATH,
                                                   '//*[@id="read-our-tos"]/main/section/div[3]/div[2]/div[1]/div/span[1]/span').text
            logging.info(f"Current server status: {current_response}")

            if current_response == 'Онлайн':
                yield 'Сервер запущен!'
                driver.quit()
                break
            elif current_response == 'Запуск...':
                yield 'Сервер запускается, подождите...'
            elif current_response == 'Підготовка...':
                yield 'Подготовка к запуску сервера'

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        yield f"Произошла ошибка: {e}"


if __name__ == "__main__":
    for status in start_minecraft_server():
        print(status)
