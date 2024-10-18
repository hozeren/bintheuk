#!/usr/bin/env python
# Autorship information
__author__ = "Hüsamettin Deniz Özeren"
__copyright__ = "Copyright 2024"
__credits__ = ["Hüsamettin Deniz Özeren"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Hüsamettin Deniz Özeren"
__email__ = "denizozeren614@gmail.com"

import os
from pathlib import Path
import RPi.GPIO as GPIO
import time
from datetime import datetime
import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from requests_html import HTMLSession
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the LED
## these are GPIO pins so it is different. Check out GPIO pins online
led_pin_blue = 2
led_pin_green = 3


# Set up the GPIO pin as an output
def led_on(pin):
    print('Led on....')
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def led_off(pin):
    print('Led off....')
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def boot(led_pin_blue, led_pin_green):
    print('Led boot....')
    led_on(led_pin_green)
    time.sleep(3)  # LED on for 1 second
    led_on(led_pin_blue)
    time.sleep(3)  # LED off for 1 second
    led_off(led_pin_blue)
    led_off(led_pin_green)
    time.sleep(3)

def get_nearest_future_date(dates_series, date_today):
    # Ensure the dates are in datetime format
    dates_series = pd.to_datetime(dates_series, format='%Y-%m-%d')
    
    # Filter out dates that are in the past
    future_dates = dates_series[dates_series >= date_today]
    
    # If no future dates are available, return None or handle accordingly
    if future_dates.empty:
        return None
    
    # Calculate the absolute difference between each future date and the reference date
    differences = (future_dates - date_today).abs()
    
    # Get the index of the smallest difference
    nearest_date_index = differences.idxmin()
    
    # Return the nearest future date
    return future_dates.loc[nearest_date_index]


# # scapre council website for bin collection dates
# def scrape_bin_dates():    
#     print('Scraping bin collection dates....')
#     link = 'https://community.newcastle.gov.uk/my-neighbourhood/your-details?uprn=004510090849&ens=423947%2C565519&address=13+Morpeth+Street%2CNewcastle+upon+Tyne%2CNE2+4AS&addresses=004510090849%3B423947%2C565519%3B13+Morpeth+Street%2CNewcastle+upon+Tyne%2CNE2+4AS'
#     headers = {
#     "connection" : "keep-alive",
#     "keep-alive" : "timeout=20, max=10000"
#     }
#     page = requests.get(link, headers=headers, timeout=(3.05, 40))
#     # page = requests.Session()
#     # page.get(link, headers=headers)
#     # session = HTMLSession()
#     # page = session.get(link)
#     # page.html.render(wait=60, timeout=1000000)
#     #find the login modal using its css selector
#     # Set up Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run in headless mode
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     # Initialize WebDriver
#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         # Navigate to the URL
#         link = 'https://community.newcastle.gov.uk/my-neighbourhood/your-details?uprn=004510090849&ens=423947%2C565519&address=13+Morpeth+Street%2CNewcastle+upon+Tyne%2CNE2+4AS&addresses=004510090849%3B423947%2C565519%3B13+Morpeth+Street%2CNewcastle+upon+Tyne%2CNE2+4AS'
#         driver.get(link)

#         # Wait for the page to load
#         WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

#         # Get the page source
#         page_source = driver.page_source
#         print(page_source)

#     finally:
#         # Close the WebDriver
#         driver.quit()
#     while True:
#         # parse the content with beautifulsoup
#         soup = BeautifulSoup(page.content, "html.parser")
#         results = soup.findAll('div', id={"binsdiv"})
#         time.sleep(5)
#         print(results)
#         t=+10
#         page = requests.get(link, headers=headers, timeout=(3.05, t))

#     return results
# try:
#     while True:
#         led_on(led_pin_green)
#         time.sleep(1)  # LED on for 1 second
#         led_off(led_pin_green)
#         time.sleep(1)  # LED off for 1 second
#         led_on(led_pin_blue)
#         time.sleep(1)  # LED off for 1 second
#         led_off(led_pin_blue)
#         time.sleep(1)
# except KeyboardInterrupt:
#     pass
# finally:
#     GPIO.cleanup()  # Clean up GPIO settings


def led_on_date():
    # this code snippet compare the dates; written by copilot partially.
    date_today = datetime.today()
    file_path = Path(__file__).parent
    df = pd.read_json(os.path.join(file_path, "bin_dates2024.json"))

    # Get the minimum dates from from get_nearest_future_date function
    blue_date = get_nearest_future_date(df['blue'], date_today)
    green_date = get_nearest_future_date(df['green'], date_today)

    # Calculate the difference in days
    day_difference_blue = abs((blue_date - date_today).days)
    day_difference_green = abs((green_date - date_today).days)
    print('Days to blue bin: ' + str(day_difference_blue))
    print('Days to green bin: ' + str(day_difference_green))


    if day_difference_blue < day_difference_green:
        if day_difference_blue < 2:
            print("Blue bin day is in two days")
            led_on(led_pin_blue)
        else:
            print("There is {} days for blue bin".format(day_difference_blue))
    else:
        if day_difference_green < 2:
            print("Green bin day is in two days")
            led_on(led_pin_green)
        else:
            print("There is {} days for green bin, IT IS NEXT!".format(day_difference_green))

if __name__ == '__main__':
    boot(led_pin_blue, led_pin_green)
    print('Boot complete....')
    # results = scrape_bin_dates()
    led_on_date()




    """
    df_blue = df['blue']
    df_green = df['green']
    df_blue = pd.to_datetime(df_blue.dropna(), format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    df_green = pd.to_datetime(df_green, format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    df_green = df_green.dropna(how='any')

    # Get the minimum dates from df_blue and df_green as strings
    min_date_blue_str = df_blue.min()
    min_date_green_str = df_green.min()

    # Convert the string dates to datetime objects
    min_date_blue = datetime.strptime(min_date_blue_str, '%Y-%m-%d')
    min_date_green = datetime.strptime(min_date_green_str, '%Y-%m-%d')

    # Calculate the difference in days
    day_difference_blue = abs((min_date_blue - date_today).days)
    day_difference_green = abs((min_date_green - date_today).days)
    print(day_difference_blue)
    print(day_difference_green)
    """