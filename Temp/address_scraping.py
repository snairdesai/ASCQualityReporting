''' This file scrapes addresses for all ASCs in the Final Data which were not found, using
their provider numbers. '''

# Importing relevant packages.
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import pyautogui

# Specifying the headless option.
options = webdriver.ChromeOptions()
options.add_argument('headless')

# Get provider numbers in DataFrame.
codeDf = pd.read_csv("missing_addresses.csv")
print(codeDf)

# Generate the list of provider numbers.
codeList = codeDf['provider_number']
codeList = codeList.values.tolist()

# Initializing a counter for the ASC number. In total, we have 580 ASCs with missing addresses.
ASC_num = 0

# Defining an data frame to store the results.
Address_Matching = pd.DataFrame(columns=['index', 'scraped_provider_number', 'scraped_npi', 'scraped_name', 'scraped_address'])

# Get ASC-Level Data and Append to DataFrame.
for code in codeList[0:581]:
    provider_number = code
    ASC_num += 1
    print("Finding ASC number: " + str(ASC_num))
    # First, we create the proper list of codes. We want these stored as strings of integers rather than floats.
    code = str(code)
    print(code)
    # Next, we initialize Chrome Driver.
    driver = webdriver.Chrome(executable_path='/Users/sameer_nair-desai/Desktop/KEY/Work/Brown_RA/ST/Tom_ASC_Analysis/Code/Python/chromedriver', options=options)
    # Now, we specify the website to scrape from.
    driver.get("https://www.qualityreportingcenter.com/en/ascqr-program/data-dashboard/ccn/")
    # Here, we find the search bar and enter the code.
    prvdr_ID = driver.find_element_by_id('CNNLookup-4298')
    prvdr_ID.send_keys(code)
    prvdr_ID.submit()
    # We give the page some time to load.
    time.sleep(2)
    # Next, we attempt to find the relevant NPI, and store it as a new variable.
    try:
        scraped_npi = driver.find_element_by_xpath('/html/body/main/section/div/div/p[1]').text
        scraped_npi = scraped_npi.split("NPI: ")[1]
        print(scraped_npi)
    # If an NPI is not found, we set the variable as an empty blank, notify the user, and continue.
    except Exception as error:
        scraped_npi = ""
        print("ASC NPI not found for index: " + str(ASC_num))
    # Now, we attempt to find the relevant name (as a check) and store as a variable.
    try:
        scraped_name = driver.find_element_by_xpath('/html/body/main/section/div/div/p[2]/b').text
        print(scraped_name)
    # If an name is not found, we set the variable as an empty blank, notify the user, and continue.
    except Exception as error:
        scraped_name = ""
        print("ASC name not found for index: " + str(ASC_num))
    # Lastly, we attempt to find our address information.
    try:
        scraped_address = driver.find_element_by_xpath('/html/body/main/section/div/div/p[2]').text
        scraped_address = scraped_address.split("\n")[1].split("Address: ")[1]
        print(scraped_address)
    except Exception as error:
        scraped_address = ""
        print("ASC address not found for index: " + str(ASC_num))
    Address_Matching = Address_Matching.append(
        {'index': ASC_num, 'scraped_provider_number': provider_number, 'scraped_npi': scraped_npi, 'scraped_name': scraped_name, 'scraped_address': scraped_address}, ignore_index=True)
    print(Address_Matching)
    # Address_Matching.to_csv('/Users/sameer_nair-desai/Desktop/KEY/Work/Brown_RA/ST/Tom_ASC_Analysis/Temp/Address_Matching.csv')

# Printing the final data.
# Address_Matching.to_csv('/Users/sameer_nair-desai/Desktop/KEY/Work/Brown_RA/ST/Tom_ASC_Analysis/Temp/Address_Matching.csv')