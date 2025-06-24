from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, unquote
import tempfile
import time

USERNAME = "dhulanageshwarao"
PASSWORD = "Kaushik@21"
TARGET = "cbitosc"

# ChromeDriver path
CHROMEDRIVER_PATH = r"C:\Users\Kaushik\Desktop\New folder\chromedriver.exe"

# Setup browser
options = Options()
options.add_argument("--start-maximized")
options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
options.add_experimental_option("detach", True)  # Keep browser open if needed

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

#Step 1: Login
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(7)

wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)
time.sleep(7)

#Step 2: Open target profile
driver.get(f"https://www.instagram.com/{TARGET}/")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
time.sleep(4)

#Step 3: Follow if not already
try:
    follow_button = driver.find_element(By.XPATH, "//header//button")
    btn_text = follow_button.text.strip().lower()
    if btn_text == "follow":
        follow_button.click()
        print("Followed the user.")
    else:
        print(f"Already following or status: '{btn_text}'.")
except Exception as e:
    print("Follow button issue:", e)

#Step 4: Extract profile data
data = {"username": TARGET}

try:
    header = driver.find_element(By.TAG_NAME, "header")

    # Full Name
    try:
        full_name = header.find_element(By.XPATH, ".//h1").text.strip()
        data["full_name"] = full_name if full_name else "N/A"
    except:
        data["full_name"] = "N/A"

    # Bio
    try:
        bio_divs = header.find_elements(By.XPATH, ".//section/div/span")
        bio_lines = [div.text.strip() for div in bio_divs if div.text.strip()]
        data["bio"] = "\n".join(bio_lines) if bio_lines else "N/A"
    except:
        data["bio"] = "N/A"

    # Link
    try:
        raw_link = header.find_element(By.XPATH, ".//a[contains(@href, 'linktr.ee')]").get_attribute("href")
        parsed = parse_qs(urlparse(raw_link).query)
        data["link"] = unquote(parsed['u'][0]) if 'u' in parsed else raw_link
    except:
        data["link"] = "N/A"

    # Stats
    try:
        stats = header.find_elements(By.XPATH, ".//ul/li")
        data["posts"] = stats[0].text.split(" ")[0]
        data["followers"] = stats[1].text.split(" ")[0]
        data["following"] = stats[2].text.split(" ")[0]
    except:
        data["posts"] = data["followers"] = data["following"] = "N/A"

except Exception as e:
    print("Error extracting data:", e)

#Step 5: Save to file
with open("cbitosc_data.txt", "w", encoding="utf-8") as f:
    for key, value in data.items():
        f.write(f"{key}: {value}\n")

print("\n Data saved to cbitosc_data.txt")
print(data)

driver.quit()
