import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# config

delay_time = 0.3

def get_one_day():
    """get data for one day"""
    # select region
    region_select = Select(driver.find_element(By.NAME, 'regions'))
    region_select.select_by_value(REGION_INPUT)
    time.sleep(delay_time)
    # select station
    station_select = Select(driver.find_element(By.NAME, 'station'))
    station_select.select_by_value(STATION_INPUT)
    time.sleep(delay_time)
    # input date
    date_input = driver.find_element(By.NAME, 'indate')
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
    time.sleep(delay_time)
    date_input.clear()
    date_input.send_keys(f"{DATE_INPUT[0:4]}/{DATE_INPUT[4:6]}/{DATE_INPUT[6:8]}")
    time.sleep(delay_time)
    download_button = driver.find_element(By.ID, "excel")
    download_button.click()
    # submit


    
# STATIC_VARIABLES
if len(sys.argv) >= 2:
    DATE_INPUT = sys.argv[1]
    REGION_INPUT = sys.argv[2]
    STATION_INPUT = sys.argv[3]
else:
    print("NO INPUT DATA FOUND :")
    DATE_INPUT = input("DATE : yyyymmdd OR yyyymm OR yyyy \n")
    REGION_INPUT = input("INSERT REGION CODE \n")
    STATION_INPUT = input("INSERT STATION CODE \n")

# handle download path
script_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(script_dir, 'downloads')
os.makedirs(download_dir, exist_ok=True)

# init chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,
    "add_experimental_option": True,
    "safebrowsing.disable_download_protection": True,
    "safebrowsing.disable_extension_blacklist": True,
    "profile.default_content_settings.popups": 0,
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
})
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--safebrowsing-disable-download-protection")
chrome_options.add_argument("--safebrowsing-disable-extension-blacklist")
chrome_options.add_argument("--disable-extensions")


driver = webdriver.Chrome(options=chrome_options)

driver.execute_cdp_cmd("Page.setDownloadBehavior", {
    "behavior": "allow",
    "downloadPath": download_dir
})

# open url

driver.get("http://www.aws-observation.tmd.go.th")
time.sleep(delay_time)

# go to download page
sidebars = driver.find_elements(By.CSS_SELECTOR, "ul.metismenu.list-unstyled#side-menu > li")
sidebars[4].click()
menu = sidebars[4].find_elements(By.CSS_SELECTOR, "ul.sub-menu.mm-collapsing.mm-collapse.mm-show > li")
for item in menu:
    if item.text == "Collection Data by Time Slot":
        item.click()
        break
time.sleep(delay_time)

# validate date data 

"""
station id is in region index+1
example 34 is in region 2
"""
regions = [
    [21,22,23,24,25,26,27,28,30,31,32,33,37,45,104,105,106,107,108],
    [34,35,36,38,39,40,41,42,43,44],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,95,96,97,98],
    [56,57,58,59,60,61,62,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,100,101,109],
    [29,47,48,50,51,52,53,55,69,85,86,87,88,89,90,91,92,94,102,103],
    [54,63,64,65,66,67,68,93]
]

if not int(STATION_INPUT) in regions[int(REGION_INPUT)-1]:
    print("REGION AND STATION NOT MATCH")
    exit()

# handle date input
if len(DATE_INPUT) == 8:
    print("LOADING DATA FOR 1 DAY")
    get_one_day()
elif len(DATE_INPUT) == 6:
    print("LOADING DATA FOR 1 MONTH")
    print("NOT IMPLEMENTED YET")
    pass
elif len(DATE_INPUT) == 4:
    print("LOADING DATA FOR 1 YEAR")
    print("NOT IMPLEMENTED YET")
    pass
else:
    print("INVALID DATE INPUT")
    exit()

# potect close browser
print("Proscess Done Press Enter to Close Browser")
input()