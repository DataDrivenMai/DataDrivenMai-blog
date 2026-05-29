"""
Description: Essential code for responsible web scraping.
"""

# Import libraries
import urllib.robotparser as urlroboparser
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

# Constants
# URL with the robots.txt file
robots_url = 'https://www.equibase.com/robots.txt'
robots_filename = './data/equibase_robots.txt'

# URL containing 10-minute interval weather data from Tokyo site on March 1-5, 2024
dates = [1, 2, 3, 4, 5]
jma_URL_base = 'https://www.data.jma.go.jp/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=2024&month=3&day=' 
jma_URL_suffix = '&view='

# One good and one bad URL to try to access
delay_time = 30
time_out = 20
URL_sample = ['https://www.data.jma.go.jp/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=2024&month=3&day=1&view=',
              'https://www.data.jma.go./stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=2024&month=3&day=1&view=']
    
# Local functions
def PeekAtWeatherData(http_resp):
    """Function to return the 10 min JMA weather data, given the HTTP requests
    AUTHOR:     Mai Tanaka (www.DataDrivenMai.com)
    DATE:       2026-05-25
    REQUIRES:   http_resp = HTTP response object returned from requests.get() function
    RETURNS:    JMA_df = dataframe containing weather data
    """
    # pandas dataframe to store the weather data
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
    JMA_df = pd.DataFrame(columns=headers_s1)
    
    # HTML parser to make sense of the Response object
    beaut_soup = BeautifulSoup(http_resp.content, "html.parser")
    
    # Find all the <table> tags
    html_tables = beaut_soup.body.find_all('table')

    # Search for the table ID
    # Search for '00:10' string in the table
    for table in html_tables:
        
        # If the '00:10' string is inside this table
        if table.find_all(string='00:10') != []:
            table_id = table.attrs['id']
            table_class = table.attrs['class'][0]
                        
    # Select all rows within the target table
    table_rows = beaut_soup.select('table#' + table_id + ' tr')
    
	# Iterate through each row in the table
    rowCount = 0
    for rowNow in table_rows:

        # Search for the data_0_0 class that contains the weather data
        list_data = rowNow.select('.data_0_0')

        if len(list_data) == 0:
            # There is no data in this row (ie. it is a column headers), so skip
            continue

        else:
            # Timestamp is the first td element in the row
            temptime = rowNow.select_one('td')
            time_now = temptime.text.strip() # Strip away the tags and excess spaces
            JMA_df.loc[rowCount, 'time'] = time_now

            # Work through each data element to extract meteorological data
            columnCount = 1
            for dataNow in list_data:
                # Extract just the data (remove tags and spaces)
                justData = dataNow.text.strip()

                # Save the data into the appropriate location and increment columnCount
                JMA_df.loc[rowCount, headers_s1[columnCount]] = justData
                columnCount = columnCount + 1

            # Increment rowCount
            rowCount = rowCount + 1

	# Return the dataframe containing the weather data
    return JMA_df

# Main script
def main():
    """Main script that reads in a robots.txt file and shows good web scraping practices including pausing between requests, exception handling and setting a timeout parameter."""

    # Create a parser for the robots.txt file and set the URL
    robots_txt = urlroboparser.RobotFileParser()
    robots_txt.set_url(robots_url)

    # Read the contents of the robots.txt file
    robots_txt.read()

    # Write out contents of the robots.txt file
    with open(robots_filename, "w") as f:
        f.write(str(robots_txt))
    
    # Access JMA Tokyo data from March 1 to 5, 2024
    for i in dates:
        # Make the appropriate URL for the date
        jma_URL = jma_URL_base + str(i) + jma_URL_suffix
        
        # HTTP GET request to jma_URL
        http_resp = requests.get(jma_URL)
        print("Request sent to URL:\n\t", jma_URL)
        
        # Wait between hits
        time.sleep(30) 
        
        # Take a peek at the weather data contained within the table
        JMA_df = PeekAtWeatherData(http_resp)
        print(JMA_df.loc[0:5, ['time', 'temperature (℃)', 'relative humidity', 'average wind speed (m/s)']])


    # Try accessing one good and one bad URL
    for i in range(0, len(URL_sample)):
        # Make the appropriate URL for the date
        jma_URL = URL_sample[i]
        
        # HTTP GET request to jma_URL with exception handling
        try:
            print("Request sent to URL:\n\t", jma_URL)
            http_resp = requests.get(jma_URL, timeout=time_out)
            
            # Need to call .raise_for_status to see if we've gotten exceptions
            http_resp.raise_for_status()
        except requests.Timeout as timeout_err: 
            # Time out exception
            print(f"The request timed out: {timeout_err}")
        except requests.RequestException as err: 
            # All other exceptions
            print(f"Some sort of error occurred: {err}")
        else:
            # Successful case
            # Take a peek at the weather data contained within the table 
            JMA_df = PeekAtWeatherData(http_resp)
            print(JMA_df.loc[0:5, ['time', 'temperature (℃)', 'relative humidity', 'average wind speed (m/s)']])

        # Wait between hits
        time.sleep(delay_time) 

if __name__ == "__main__":
    main()
