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

09/15/23:
MOD: Functionality works + resolved errors
AUTHOR: Ian Chavez
COMMENT: n/a

====================== END OF MODIFICATION HISTORY ============================
"""
# Imports
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import certifi

URL = "https://sjsuparkingstatus.sjsu.edu/"

def scrape_and_store_parking_data(data_snapshots):
    try:
        response = requests.get(URL, verify=cert_path)

        # if success
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            sjsu_main = soup.find('main', class_='sjsu-main')
            if sjsu_main:
                
                wrap = sjsu_main.find('div', class_='wrap')
                if wrap:
                    
                    garage = wrap.find('div', class_='garage')
                    if garage:
                        
                        garage_text_elements = garage.find_all('p', class_='garage__text')
                        
                        current_time = datetime.now()
                        snapshot_data = {
                            'time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                            'day_of_week': current_time.strftime("%A")
                        }

                        for garage_text_element in garage_text_elements:
                            
                            parking_percentage_element = garage_text_element.find('span', class_='garage__fullness')

                            if parking_percentage_element:
                                parking_percentage = parking_percentage_element.text.strip()

                                garage_name_element = garage_text_element.find_previous('h2', class_='garage__name')

                                if garage_name_element:
                                    garage_name = garage_name_element.text.strip()
                                    
                                    # add parking percentage to snapshot dictionary
                                    snapshot_data[garage_name] = parking_percentage
                            else:
                                print("Could not find 'garage__fullness' element within a 'garage__text' element.")
                        data_snapshots.append(snapshot_data)
                        return data_snapshots

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
                        print(f"{garage}: {percentage} ")
            data_snapshots.clear()
        else:
            print("No data retrieved.")
        
        # wait 4 minutes before the next scrape
        time.sleep(240)  
