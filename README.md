# sjsuparking4me

## Description
This is a personal project by Ian Chavez, CS major at San Jose State University. The goal of this project is to create a web application that will allow users to view parking availability in real time.

This will pull from the SJSU Parking Status website (link: https://sjsuparkingstatus.sjsu.edu/) and display the information in a more user friendly way with additional functionality of estimating potential parking at a the user's given input time.

-----------------------------------------Dev Journal-----------------------------------------
9/15/2023:

Pull current % of parking availability from SJSU Parking Status website (https://sjsuparkingstatus.sjsu.edu) and store it in a database. From real experience, the website seems to update every 4 minutes after refreshing.

Store data per each garage (North, West, South, South Campus). Potentially use a dictionary to store the data? (key: garage name, value: % availability)


9/16/2023:

WebScraper.py works as intended, returning a dictionary with the garage name as the key and the % availability as the value.

Now storing the data in a database. Maybe SQLite3? More experience with SQL so might as well.
Possible Schema:
CREATE TABLE IF NOT EXISTS parking_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_of_week VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    garage_name VARCHAR(255) NOT NULL,
    percentage DECIMAL(5, 2) NOT NULL
);

---------------------------------------End Dev Journal---------------------------------------