from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import concurrent.futures

# Setup Chrome options
options = Options()
options.add_argument("--headless")
driver_path = ChromeDriverManager().install()

# Prepare date matching logic
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
reference_date = datetime(2025, 4, 16)

def infer_date(text):
    for wd in weekdays:
        if wd in text:
            target_wd = weekdays.index(wd)
            ref_wd = reference_date.weekday()
            delta = (ref_wd - target_wd) % 7
            return (reference_date - timedelta(days=delta)).strftime('%Y-%m-%d')
    return ""

def fetch_flight_links():
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.get("https://www.flightaware.com/live/findflight?origin=VIDP&destination=VOBL")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Results"]/tbody/tr'))
    )

    rows = driver.find_elements(By.XPATH, '//*[@id="Results"]/tbody/tr')
    data = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 7:
            try:
                link = cols[1].find_element(By.TAG_NAME, "a").get_attribute("href")
                data.append({
                    "Airline": cols[0].text.strip(),
                    "Flight Number": cols[1].text.strip(),
                    "Aircraft": cols[2].text.strip(),
                    "Status": cols[3].text.strip(),
                    "Departure": cols[4].text.strip(),
                    "Departure Date": infer_date(cols[4].text.strip()),
                    "Gate/Terminal": cols[5].text.strip(),
                    "Arrival": cols[6].text.strip(),
                    "Arrival Date": infer_date(cols[6].text.strip()),
                    "Flight URL": link
                })
            except:
                continue
    driver.quit()
    return data

def fetch_delay_status(flight):
    try:
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
        driver.get(flight["Flight URL"])

        try:
            dep_status = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="flightPageTourStep1"]/div[3]/div[1]/span[3]/div/span'))
            ).text.strip()
        except:
            dep_status = "Unavailable"

        try:
            arr_status = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="flightPageTourStep1"]/div[3]/div[2]/span[3]/div/span'))
            ).text.strip()
        except:
            arr_status = "Unavailable"

        flight["Departure Delay Status"] = dep_status
        flight["Arrival Delay Status"] = arr_status

        print(f"✅ {flight['Flight Number']}: {dep_status} / {arr_status}")
        driver.quit()
        return flight

    except Exception as e:
        print(f"⚠ Error fetching flight {flight['Flight Number']}: {e}")
        return flight

# Main flow
data = fetch_flight_links()

# Parallel delay status fetch
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_delay_status, data))

# Save to CSV
df = pd.DataFrame(results)
output_path = os.path.abspath("detailed_flight_data32.csv")
df.to_csv(output_path, index=False)
print(f"\n✅ Optimized data saved to: {output_path}")
