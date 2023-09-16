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
from datetime import datetime
import time

URL = "https://sjsuparkingstatus.sjsu.edu/"

# Function to scrape parking data and store snapshots
def scrape_and_store_parking_data(data_snapshots):
    try:
        response = requests.get(URL, verify=False)

        # If successful, proceed with processing the data
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            sjsu_main = soup.find('main', class_='sjsu-main')
            if sjsu_main:
                print("Found 'sjsu-main' element.")
                
                wrap = sjsu_main.find('div', class_='wrap')
                if wrap:
                    print("Found 'wrap' element.")
                    
                    garage = wrap.find('div', class_='garage')
                    if garage:
                        print("Found 'garage' element.")
                        
                        garage_text_elements = garage.find_all('p', class_='garage__text')
                        
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        snapshot_data = {'time': current_time}

                        for garage_text_element in garage_text_elements:
                            print("Found 'garage__text' element.")
                            
                            parking_percentage_element = garage_text_element.find('span', class_='garage__fullness')

                            if parking_percentage_element:
                                parking_percentage = parking_percentage_element.text.strip()

                                # find garage name within the <h2> element
                                garage_name_element = garage_text_element.find_previous('h2', class_='garage__name')

                                if garage_name_element:
                                    print("Found 'garage__name' element.")
                                    
                                    garage_name = garage_name_element.text.strip()
                                    print(f"Garage Name: {garage_name}")
                                    print(f"Parking Percentage: {parking_percentage}")
                                    
                                    # add parking percentage to snapshot dictionary
                                    snapshot_data[garage_name] = parking_percentage
                            else:
                                print("Could not find 'garage__fullness' element within a 'garage__text' element.")

                        data_snapshots.append(snapshot_data)

                else:
                    print("Could not find 'garage' element.")
                    return None
            else:
                print("Could not find 'wrap' element.")
                return None
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == '__main__':
    data_snapshots = []

    while True:
        parking_data = scrape_and_store_parking_data(data_snapshots)
        if parking_data:
            print("Parking Data:")
            for snapshot in data_snapshots:
                print("Snapshot Time:", snapshot['time'])
                for garage, percentage in snapshot.items():
                    if garage != 'time':
                        print(f"{garage}: {percentage}")
        else:
            print("No data retrieved.")
        
        # wait 4 minutes before the next scrape
        time.sleep(240)  
