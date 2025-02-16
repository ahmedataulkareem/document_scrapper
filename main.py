import time
import random
import pytesseract
import cv2
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Mimic human-like behavior with randomized delays
def human_delay(min_delay=2, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Set up Chrome options to avoid detection
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

# Random User-Agent rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]
options.add_argument(f"user-agent={random.choice(user_agents)}")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL to access
url = "https://voters.eci.gov.in/download-eroll?statecode=S25"
driver.get(url)

# Wait until the page is loaded
wait = WebDriverWait(driver, 15)  # Adjust timeout as needed
human_delay(5, 8)

# Function to solve CAPTCHA using Tesseract OCR
def solve_captcha():
    captcha_element = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')]")))
    captcha_image_path = "captcha.png"
    captcha_element.screenshot(captcha_image_path)

    # Process image to improve OCR accuracy
    image = cv2.imread(captcha_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    processed_image = Image.fromarray(thresh)

    captcha_text = pytesseract.image_to_string(processed_image, config="--psm 6").strip()
    print(f"[INFO] Solved CAPTCHA: {captcha_text}")
    return captcha_text

# Function to fill form and download the PDF
def fill_form_and_download():
    try:
        # Wait for State dropdown and select value
        state_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='stateCode']")))
        Select(state_dropdown).select_by_visible_text("West Bengal")
        human_delay()

        # Wait for District dropdown and select value
        district_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='district']")))
        Select(district_dropdown).select_by_visible_text("KOLKATA NORTH")
        human_delay()
        input("[INFO] Please select the Assembly Constituency manually and press Enter to continue...")
        human_delay(8)

        # Wait for Language dropdown and select value
        language_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='langCd']")))
        Select(language_dropdown).select_by_visible_text("ENG")
        human_delay()


        # Solve CAPTCHA
        captcha_text = solve_captcha()
        captcha_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='captcha']")))
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)

        # Click the download button (Final Roll - 2025)
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@role='cell']/img[@alt='download icon']")))
        download_button.click()
        print("[INFO] Download button clicked.")

        # Check if CAPTCHA is incorrect
        human_delay(5, 10)
        if "captcha" in driver.page_source.lower():
            print("[ERROR] CAPTCHA failed. Retrying...")
            return False
        else:
            print("[INFO] Download initiated successfully.")
            return True

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

# Retry mechanism if CAPTCHA is incorrect
max_attempts = 5
for attempt in range(1, max_attempts + 1):
    print(f"[INFO] Attempt {attempt} of {max_attempts}")
    if fill_form_and_download():
        break
    else:
        driver.refresh()  # Reload the page
        human_delay(5, 8)

driver.quit()
