# coding: utf-8
# NAME: WebScraper.py
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

11/14/23:
MOD: Test Certifi + Google Sheet compatibility
AUTHOR: Ian Chavez
COMMENT:
    - Test Certifi: Doesn't work, issue with SSL certificate? SJSU side error?
        Reverting back to verify=False
    - Google Sheet compatibility: Works, data is being sent to Google Sheet

====================== END OF MODIFICATION HISTORY ============================
"""
# Imports
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import gspread
from config import GOOGLE_SHEETS_CREDENTIALS

URL = "https://sjsuparkingstatus.sjsu.edu/"
worksheet_map = {
    "Monday": "Monday",
    "Tuesday": "Tuesday",
    "Wednesday": "Wednesday",
    "Thursday": "Thursday",
    "Friday": "Friday",
    "Saturday": "Saturday",
    "Sunday": "Sunday",
}


def scrape_and_store_parking_data(data_snapshots):
    try:
        response = requests.get(URL, verify=False)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            sjsu_main = soup.find("main", class_="sjsu-main")
            if sjsu_main:
                wrap = sjsu_main.find("div", class_="wrap")
                if wrap:
                    garage = wrap.find("div", class_="garage")
                    if garage:
                        garage_text_elements = garage.find_all(
                            "p", class_="garage__text"
                        )

                        current_time = datetime.now()
                        snapshot_data = {
                            "time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "day_of_week": current_time.strftime("%A"),
                        }

                        for garage_text_element in garage_text_elements:
                            parking_percentage_element = garage_text_element.find(
                                "span", class_="garage__fullness"
                            )

                            if parking_percentage_element:
                                parking_percentage = (
                                    parking_percentage_element.text.strip()
                                )

                                garage_name_element = garage_text_element.find_previous(
                                    "h2", class_="garage__name"
                                )

                                if garage_name_element:
                                    garage_name = garage_name_element.text.strip()

                                    # add parking percentage to snapshot dictionary
                                    snapshot_data[garage_name] = parking_percentage
                            else:
                                print(
                                    "Could not find 'garage__fullness' element within a 'garage__text' element."
                                )
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


def clean_data(data_snapshots):
    # prep data for Google Sheets --> convert percentages to integers
    for snapshot in data_snapshots:
        for garage, percentage in snapshot.items():
            if garage != "time" and garage != "day_of_week":
                snapshot[garage] = int(percentage.replace("%", ""))
    return data_snapshots


def access_sheet():
    gc = gspread.service_account(GOOGLE_SHEETS_CREDENTIALS)
    sh = gc.open("SJSU Parking Status Data")

    # check date and choose correct worksheet
    sheet_name = worksheet_map[datetime.now().strftime("%A")]
    if sheet_name is not None:
        worksheet = sh.worksheet(sheet_name)
    else:
        print("Error: Invalid day of the week.")
        return None

    return worksheet


def upload_data_gsheet(data_snapshots, worksheet):
    try:
        # Prepare the data for appending to the worksheet
        values = [
            [
                snapshot["time"],
                snapshot["South Garage"],
                snapshot["West Garage"],
                snapshot["North Garage"],
                snapshot["South Campus Garage"],
            ]
            for snapshot in data_snapshots
        ]

        # Append the prepared data to the worksheet
        worksheet.append_rows(values, value_input_option="USER_ENTERED")

        print("Data uploaded to Google Sheet successfully.")
    except Exception as e:
        print(f"An error occurred while uploading data to Google Sheet: {str(e)}")


if __name__ == "__main__":
    data_snapshots = []

    while True:
        print("\n--- Scraping data ---")
        parking_data = scrape_and_store_parking_data(data_snapshots)
        print("\n--- Parking data ---")
        print(parking_data)
        print("--------------------")

        print("\n--- Cleaning data ---")
        parking_data = clean_data(parking_data)
        print("\n--- Cleaned data ---")
        print(parking_data)
        print("--------------------")

        print("\n--- Accessing GSheet ---")
        current_sheet = access_sheet()
        print("------------------------")

        print("\n--- Uploading to GSheet ---")
        if current_sheet is not None:
            upload_data_gsheet(parking_data, current_sheet)
        print("---------------------------")

        # wait 4 minutes before the next scrape
        time.sleep(240)

"""
        if parking_data:
            print("Parking Data:")
            for snapshot in data_snapshots:
                print("Snapshot Time:", snapshot['time'])
                for garage, percentage in snapshot.items():
                    if garage != 'time':
                        print(f"{garage}: {percentage}")
            data_snapshots.clear()
        else:
            print("No data retrieved.")
"""
