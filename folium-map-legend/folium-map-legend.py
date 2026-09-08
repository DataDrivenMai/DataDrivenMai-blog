"""
Description: Essential code for scraping and parsing 10-min weather data from the Japan Meteorological Agency (JMA) website using Python.
"""

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import pytz

# Constants
test_date = (2024, 3, 9) # test date specified by user
jma_URL = 'https://www.data.jma.go.jp/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=2024&month=3&day=9&view=' # URL containing 10-minute interval weather data from Tokyo site on March 9, 2024
dirName = 'data/'
fileName = 'jma_weather_scraping_python.csv'
    
# Local functions
def ConvertDateTime(row_of_data, target_tz, target_date):
	"""Function to take in a row of data, extract the time stamp, convert it to a datetime object in a local time zone
	AUTHOR: Mai Tanaka (www.DataDrivenMai.com)
	DATE: 2026-03-31
	REQUIRES: row_of_data = html table row where the first <td> cell contains the time in the form of %H:%M
			  target_tz = target timezone as an pytz.timezone object
			  target_date = (year, month , day) tuple to assign to the datetime object
	RETURNS:  output_datetime = datetime object in the specified local timezone
	"""

	# Split up target_date tuple into year, month and day
	target_year = target_date[0]
	target_month = target_date[1]
	target_day = target_date[2]

	# Timestamp is the first td element in the row
	temptime = row_of_data.select_one('td')

	# Strip away the tags and excess spaces
	temptime = temptime.text.strip()

	# The last timestamp may be 0:00 for the next day, which may cross over into next month or even year
	if (temptime == '24:00'):
		# Set output_datetime as 23:59 of the current day, then add one minute.
		# This should deal with changes in the day, month or even the year
		deltaTime = dt.timedelta(minutes=1)
		tempDateTime = dt.datetime(target_year, target_month, target_day, 23, 59) + deltaTime

	else:
		# Otherwise, extract the hour and minutes and use that as the hour and minute
		temptime = dt.datetime.strptime(temptime, '%H:%M')
		tempDateTime = dt.datetime(target_year, target_month, target_day, temptime.hour, temptime.minute)

	# Attach a time zone
	output_datetime = target_tz.localize(tempDateTime)

	# Return the datetime
	return output_datetime


def ConvertKanji2NESW(kanji_windDir):
    """Function to convert the wind direction from kanji to English
    AUTHOR:     Mai Tanaka (www.DataDrivenMai.com)
    DATE:       2026-03-31
    REQUIRES:   kanji_windDir = Full kanji indicating wind direction (eg. '北東')
    RETURNS:    english_windDir = Wind direction in English in N/E/S/W notation (eg. 'NE')
    """
    # Start with an empty string
    english_windDir = ''

    # Handle the special case: 静穏 (tranquil or no wind)
    if kanji_windDir == '静穏':
        english_windDir = 'tranquil'
        return english_windDir

    # Kanji to character (NESW) conversion, character-by-character
    for kanji_char in kanji_windDir:
        if kanji_char == '北':
            english_windDir = english_windDir + 'N'
        if kanji_char == '東':
            english_windDir = english_windDir + 'E'
        if kanji_char == '南':
            english_windDir = english_windDir + 'S'
        if kanji_char == '西':
            english_windDir = english_windDir + 'W'

    # Return English wind direction
    return english_windDir


# Main script
def main():
    """Main script that scrapes, parses and saves tabular weather data as a CSV file."""

    # Local contants
    JMA_tz = pytz.timezone('Asia/Tokyo') # Create a time zone in Japan time
    
    # The Tokyo observation site (type s1) has 11 columns of data
    headers_s1 = (['time',
                'local atmospheric pressure (hPa)',
                'sea level pressure (hPa)',
                'precipitation (mm)',
                'temperature (℃)',
                'relative humidity',
                'average wind speed (m/s)',
                'average wind direction',
                'max wind speed (m/s)',
                'max wind direction',
                'sunshine (minutes)'])

    # If you are using a 'a1' type observation site, use the headers below
    headers_a1 = (['time',
                'precipitation (mm)',
                'temperature (℃)',
                'relative humidity',
                'average wind speed (m/s)',
                'average wind direction',
                'max wind speed (m/s)',
                'max wind direction',
                'sunshine (minutes)'])

    # Specify the header you'll be using in the final dataframe
    headers_now = headers_s1 # Change to headers_a1 if using 'a1' type observation site
    step6_df = pd.DataFrame(columns=headers_now)

    # HTTP GET request to jma_URL
    # Execute care to avoid running multiple requests in a very short period of time
    step2_resp = requests.get(jma_URL)
    print("Request sent to URL:\n\t", jma_URL)

    # HTML parser to make sense of the Response object
    step3_soup = BeautifulSoup(step2_resp.content, "html.parser")
    print("Parsed HTML content with BeautifulSoup")

    # Find all the <table> tags
    step4_tables = step3_soup.body.find_all('table')

    # Search for the table ID
    # Search for '00:10' string in the table
    for table in step4_tables:
        
        # If the '00:10' string is inside this table
        if table.find_all(string='00:10') != []:
            step4_id = table.attrs['id']
            step4_class = table.attrs['class'][0]
            print('\tFound the target table with ID', step4_id, 'and class', step4_class)
                        
    # Select all rows within the target table
    step5_tableRows = step3_soup.select('table#' + step4_id + ' tr')

    # Iterate through each row in the table
    rowCount = 0
    for rowNow in step5_tableRows:

        # Search for the data_0_0 class that contains the weather data
        list_data = rowNow.select('.data_0_0')

        if len(list_data) == 0:
            # There is no data in this row (ie. it is a column headers), so skip
            #print("Skipping row: ", rowNow)
            continue

        else:
            # Convert time from string to datetime with time zone and assign it
            time3 = ConvertDateTime(rowNow, JMA_tz, test_date)
            step6_df.loc[rowCount, headers_now[0]] = time3

            # Work through each data element to extract meteorological data
            columnCount = 1
            for dataNow in list_data:
                # Extract just the data (remove tags and spaces)
                justData = dataNow.text.strip()

                # If the data type is wind direction, convert from Kanji to alphabet
                if "wind direction" in headers_now[columnCount]:
                    justData = ConvertKanji2NESW(justData)

                # Save the data into the appropriate location and increment columnCount
                step6_df.loc[rowCount, headers_now[columnCount]] = justData
                columnCount = columnCount + 1

            # Increment rowCount
            rowCount = rowCount + 1
    print("Extracted weather data from HTML table into a DataFrame")
    
    # Save the DataFrame to a CSV file
    savefileName = dirName + fileName
    step6_df.to_csv(savefileName, index=False, encoding='utf-8')
    print("Saved the DataFrame to a CSV file:\n\t", savefileName)

    # When loading the CSV file, use parse_dates to convert the time column back into datetime objects
    step7_df = pd.read_csv(savefileName, parse_dates=['time'])
    print("Loaded the CSV file into a DataFrame with parse_dates")

if __name__ == "__main__":
    main()
