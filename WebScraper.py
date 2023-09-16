# coding: utf-8 
#NAME: WebScraper.py
"""
AUTHOR: Ian Chavez

Unpublished-rights reserved under the copyright laws of the United States.

This data and information is proprietary to, and a valuable trade secret of Ian Chavez. It is given in confidence by
Ian Chavez. Its use, duplication, or disclosure is subject to the restrictions set forth in the License Agreement under which it has been
distributed.

Unpublished Copyright © 2023 Ian Chavez

All Rights Reserved
"""
"""
========================== MODIFICATION HISTORY ==============================
09/15/23:
MOD: Creation of file and initial function
AUTHOR: Ian Chavez
COMMENT: n/a

====================== END OF MODIFICATION HISTORY ============================
"""
# Imports
import requests
from bs4 import BeautifulSoup

URL = "https://sjsuparkingstatus.sjsu.edu/"

# Function to scrape parking data
def scrape_parking_data():
    try:
        response = requests.get(URL)

        # If successful, proceed with processing the data
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element that contains the parking data
            parking_data = soup.find('div', class_='your-parking-data-class')

            # Extract and process the parking data
            if parking_data:
                parking_data = parking_data.text.strip()
                return parking_data
            else:
                print("Could not find parking data element on the page.")
                return None
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == '__main__':
    parking_data = scrape_parking_data()
    if parking_data:
        print("Parking Data:")
        print(parking_data)
    else:
        print("No data retrieved.")
