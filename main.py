import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha

# --- CONFIGURATION ---
ORANGE_URL = "https://orangecarrier.com/login" # Apnar login link
TELEGRAM_BOT_TOKEN = "8969489020:AAGUzQbKb87tLXLTJTwZn2N9Nzl7n8B9eWU"
TELEGRAM_CHAT_ID = "-1003937969013"
TWOCAPTCHA_API_KEY = "6f4b64cb137f8fc6be195583595afbb6"
USERNAME = "nakibulyt26@gmail.com"
PASSWORD = "@Nakibul2"

def solve_captcha(driver):
    try:
        # Site key ba page URL khuje ber kora jekhane captcha ache
        solver = TwoCaptcha(TWOCAPTCHA_API_KEY)
        # Jodi reCAPTCHA hoy tar sitekey collect korte hobe element theke
        sitekey_element = driver.find_element(By.CLASS_NAME, "g-recaptcha")
        sitekey = sitekey_element.get_attribute("data-sitekey")
        
        result = solver.recaptcha(
            sitekey=sitekey,
            url=driver.current_url
        )
        code = result['code']
        
        # Captcha token inject korar script
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{code}';")
        print("Captcha successfully solved and applied!")
    except Exception as e:
        print(f"Captcha solving failed: {e}")

def send_voice_to_telegram(audio_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVoice"
    with open(audio_path, 'rb') as voice_file:
        payload = {'chat_id': TELEGRAM_CHAT_ID}
        files = {'voice': voice_file}
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            print("Voice OTP successfully forwarded to Telegram!")
        else:
            print(f"Failed to send voice: {response.text}")

def main():
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 1. Login Page Open
        driver.get(ORANGE_URL)
        time.sleep(3)

        # 2. Fill Credentials
        driver.find_element(By.NAME, "username").send_keys(USERNAME) # Field name website onujayi change hote pare
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)

        # 3. Handle Captcha (Jodi thake)
        if len(driver.find_elements(By.CLASS_NAME, "g-recaptcha")) > 0:
            solve_captcha(driver)

        # 4. Submit Login
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(5)

        # 5. Monitor Live Calls & Capture Audio
        print("Monitoring live calls for voice OTP...")
        while True:
            # Live calls page ba element check korar logic
            # Jodi kono notun call ba audio element pawa jay, take download korte hobe:
            # Example: audio_url = driver.find_element(By.TAG_NAME, "audio").get_attribute("src")
            
            # Audio download kore local-e save korar por:
            # audio_file_path = "downloaded_otp.mp3"
            # send_voice_to_telegram(audio_file_path)
            
            time.sleep(10) # Prottek 10 second por por check korbe

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
