from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from time import sleep
import requests
import pandas as pd


'''
scrapes flight info from www.Kayak.com 
returns dataframe
'''
def get_flight_info(origin, destination, startdate, enddate, sort_by):
    url = "https://www.kayak.com/flights/" + origin + "-" + destination + "/" + startdate + "/" + enddate + "?sort=" + sort_by

    print("... scraping at " + url + ' ...\n')

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    driver.get(url)

    soup=bs(driver.page_source, 'lxml')

    flights = soup.find_all('div', attrs={'class': "nrc6-wrapper"})

    dep_times = []
    arr_times = []
    prices = []
    links = []

    for flight in flights:
            # times
            times_section = flight.find_all_next('div', attrs={'class': "vmXl vmXl-mod-variant-large"})
            dep_string = times_section[0].text
            if dep_string[-1] == '1':
                dep_string = dep_string[:-2]
            dep_times.append(dep_string)
            arr_string = times_section[1].text
            if arr_string[-1] == '1':
                    arr_string = arr_string[:-2]
            arr_times.append(arr_string)
            # price 
            price_string = flight.find('div', attrs={'class': 'f8F1-price-text'}).text[1:]
            prices.append(int(price_string))
            # link  
            link_string = "https://www.kayak.com/flights/" + flight.find('div', attrs={'class': 'oVHK'}).find('a').get('href')
            links.append(link_string)

    driver.quit()
    df = pd.DataFrame({"origin" : origin,
                        "destination" : destination,
                        "startdate" : startdate,
                        "enddate" : enddate,
                        "price": prices,
                        "currency": "USD",
                        "deptime": [str(time) for time in dep_times],
                        "arrtime": [str(time) for time in arr_times]
                        })
    return df


'''
example input: 
    origin = 'SFO'
    destination = 'LAX'
    startdate = '2023-07-17'
    enddate = '2023-07-24'
'''
print('\n')
origin = input("Input airport code to depart from (ex - 'SFO'): ")
destination = input("Input airport code of arrival airport (ex - LAX): ")
startdate = input("Input desired date of departure, year-month-day (xxxx-xx-xx): ")
enddate = input("Input desired date of return,year-month-day (xxxx-xx-xx): ")
sort_by = input("Input letter - sort by (a) price, (b) best, (c) quickest: ")
print('\n')

valid = False
while not valid: 
    valid = True
    if sort_by == "a":
                sort_by = "price_a"
    elif sort_by == "b":
                sort_by = "bestflight_a"
    elif sort_by == "c":
                sort_by = "duration_a"
    else:
        valid = False
        print("Invalid Input")
        sort_by = input("Input letter - sort by (a) price, (b) best, (c) quickest: ")


print(get_flight_info(origin, destination, startdate, enddate, sort_by))


