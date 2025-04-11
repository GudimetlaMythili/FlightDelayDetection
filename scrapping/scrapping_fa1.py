from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime, timedelta

# Setup
options = Options()
# options.add_argument("--headless")  # Optional: use it when running in background
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the page
driver.get("https://www.flightaware.com/live/findflight?origin=VIDP&destination=VOBL")
time.sleep(5)

# Weekday mapping and reference date (Today is Friday, April 11, 2025)
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
reference_date = datetime(2025, 4, 11)  # Known date for 'Fri'

# Function to extract and infer date from field like "Fri 11:30AM IST"
def infer_date(text):
    if text:
        for wd in weekdays:
            if wd in text:
                target_wd = weekdays.index(wd)
                ref_wd = reference_date.weekday()
                delta = (ref_wd - target_wd) % 7
                return (reference_date - timedelta(days=delta)).strftime('%Y-%m-%d')
    return ""

# Find all table rows
rows = driver.find_elements(By.XPATH, '//*[@id="Results"]/tbody/tr')

# Store data
all_flight_data = []

for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if len(columns) >= 7:
        departure = columns[4].text.strip()
        arrival = columns[6].text.strip()

        flight = {
            "Airline": columns[0].text.strip(),
            "Flight Number": columns[1].text.strip(),
            "Aircraft": columns[2].text.strip(),
            "Status": columns[3].text.strip(),
            "Departure": departure,
            "Departure Date": infer_date(departure),
            "Gate/Terminal": columns[5].text.strip(),
            "Arrival": arrival,
            "Arrival Date": infer_date(arrival)
        }
        all_flight_data.append(flight)

# Save to CSV
df = pd.DataFrame(all_flight_data)
df.to_csv("flight_data.csv", index=False)
print("✅ Saved with both Departure and Arrival Dates in 'flight_data.csv'")

driver.quit()
