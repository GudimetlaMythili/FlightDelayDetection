from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Chrome options
options = Options()
#options.add_argument("--headless")  # Run without opening browser
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Create Service and WebDriver properly
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open FlightAware page
url = "https://www.flightaware.com/live/findflight?origin=VIDP&destination=VOBL"
driver.get(url)

time.sleep(5)  # Wait for page to load

# Collect flight data
flight_data = []
#print(driver.page_source[:1000])  # Print first 1000 characters of page source

flights = driver.find_elements(By.CSS_SELECTOR, "div.flightPageResults > div")
flight_number = driver.find_element(By.XPATH, '//*[@id="Results"]/tbody/tr[75]/td[2]/span/a').text
print(flight_number)  # Outputs: AI514
for flight in flights:
    try:
        

        route = flight.find_element(By.CSS_SELECTOR, "div.flightPageResultsAirports").text
        dep_arr_time = flight.find_element(By.CSS_SELECTOR, "div.flightPageResultsTimes").text

        flight_data.append({
            "Flight Number": flight_number,
            "Route": route,
            "Departure & Arrival": dep_arr_time
        })

    except Exception:
        continue

driver.quit()

# Save to CSV
df = pd.DataFrame(flight_data)
df.to_csv("flight_data.csv", index=False)

print("✅ Data saved to 'flight_data.csv'")
