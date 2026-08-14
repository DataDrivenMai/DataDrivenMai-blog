"""
Description: Essential code for converting Japanese dates in real data into their Gregorian calendar equivalent.
"""

# Import libraries
import pandas as pd
import re

# Constants
# Filename of data to read
fileName_read = './data/ame_master_20260324.csv'
# Filename to save the output CSV
fileName_save = './data/japanese_gregorian_calendar_python.csv'
    
# Local functions
def ConvertJapaneseDates2Gregorian(str_match):
    """Convert a date in the Japanese calendar to the Gregorian calendar.
    AUTHOR: Mai Tanaka (www.DataDrivenMai.com)
	DATE: 2026-08-13
	REQUIRES: str_match = tuple of the Japanese date in the form (era, year, month, day)
    PROMISES: return_str = string of the date in the Gregorian calendar in the form 'YYYY-MM-DD'
    """

    # Convert year number, month and day from strings into integers
    # Indices 0 and 1 are associated with the year
    era = str_match[0]
    year = str_match[1]

    # If we have '元', convert it to 1
    if year == '元':
        year = 1
    else:
        year = int(year)

    # Indices 2 and 3 are associated with the month and day
    month = int(str_match[2])
    day = int(str_match[3])

    # Convert era names into Gregorian years 
    if '昭' in era:
        gregorian_year = year + 1925
    elif '平' in era:
        gregorian_year = year + 1988
    elif '令' in era:
        gregorian_year = year + 2018
    else:
        raise ValueError("Unknown era: {}".format(era))

    # Format the output as yyyy-mm-dd
    return_str = "{}-{:02d}-{:02d}".format(gregorian_year, month, day)		
    return return_str


# Main script
def main():
    """Main script that reads in Japanese dates from a CSV file, converts them into the Gregorian calendar equivalent, then saves the output as a CSV file."""

    # Read the real data and extract just the dates column
    amedas_df = pd.read_csv(fileName_read, encoding='CP932')
    japanese_dates = amedas_df['観測開始年月日']

    # Two regular expressions
    amp_re = r'#'
    date_re = r'([昭平令])\.?(元|\d+)\.(\d+)\.(\d+)'

    # Empty dataframe
    df_dates = pd.DataFrame()

    for i in range(0, len(japanese_dates)):
        # The observation start date
        observation_date = japanese_dates[i]

        # Find matches to the two regular expressions
        amp_match = re.search(amp_re, observation_date)
        date_match = re.findall(date_re, observation_date)
        
        # Temporary storage of the dates
        dates = []

        if amp_match:
            dates.append('1974-11-01')
        if date_match:
            for j in range(len(date_match)):
                # Convert the date to the Gregorian calendar
                new_date = ConvertJapaneseDates2Gregorian(date_match[j])
                dates.append(new_date)
        
        # Once dates are found, insert them into dataframe
        # Insert the original date
        df_dates.loc[i, 'original observation_date'] = observation_date

        # Insert the first date we found as rainfall data collection start date
        df_dates.loc[i, 'observation_start_date_rain'] = dates[0]

        # For all other weather data, the start date for records depends on whether we have a second date or not
        if len(dates) == 2:
            other_date = dates[1]
        else:
            other_date = dates[0]
        df_dates.loc[i, 'observation_start_date_other'] = other_date

    # Save the output as a CSV file
    df_dates.to_csv(fileName_save, index=False, encoding='utf-8')

if __name__ == "__main__":
    main()
