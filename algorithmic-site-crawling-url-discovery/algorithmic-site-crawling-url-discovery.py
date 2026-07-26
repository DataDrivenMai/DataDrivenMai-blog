"""
Description: Essential code to algorithmically crawl, scrape and parse the Japan Meteorological Agency (JMA) website HTML to automatically discover the unique identifiers needed to generate the URL of each JMA weather station.
"""

# Import libraries
import re
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
import json

# Constants
jma_URLs_comp = {
    'wakkanai': 'https://www.data.jma.go.jp/stats/etrn/view/10min_s1.php?prec_no=11&block_no=47401&year=2024&month=3&day=9&view=',
    'abashiri': 'https://www.data.jma.go.jp/stats/etrn/view/10min_s1.php?prec_no=17&block_no=47409&year=2024&month=3&day=9&view=', 
    'akan': 'https://www.data.jma.go.jp/stats/etrn/view/10min_a1.php?prec_no=19&block_no=0096&year=2024&month=3&day=9&view=',
    'tokyo': 'https://www.data.jma.go.jp/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=2024&month=3&day=9&view=', 
    'hakone': 'https://www.data.jma.go.jp/stats/etrn/view/10min_a1.php?prec_no=46&block_no=0390&year=2024&month=3&day=9&view=', 
    'nakatane': 'https://www.data.jma.go.jp/stats/etrn/view/10min_a1.php?prec_no=88&block_no=0897&year=2024&month=3&day=9&view=',
}
# URL to the starting map interface of Japan
url_japan_map = 'https://www.data.jma.go.jp/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view='
# The template of the URL
re_URL = r'https://www.data.jma.go.jp/stats/etrn/view/10min_([as])1.php\?prec_no=(\d+)&block_no=(\d+)&year=2024&month=3&day=9&view='
# File path to save the final dictionary
fileName = './data/amedas_prec_block_no_dict.json'
    
# Local functions


# Main script
def main():
    """Main script that algorithmically crawls the JMA website to automatically retrieve the URL identifiers for each weather station."""

    # Highlight the differences in the URLs of different weather stations
    print('Highlighting the differences in the URLs of different weather stations')

    # Work through each URL
    for key, value in jma_URLs_comp.items():

        # Find the part that matches the template URL
        URL_match = re.search(re_URL, value)

        # The regex extracts three sections that differ in the URL. Print them out with different colors
        print('\t', key.capitalize())
        print('data.jma.go.jp/stats/etrn/view/10min_', end="")
        print(f"\033[1;31m{URL_match.string[URL_match.start(1):URL_match.end(1)]}\033[0m", end="")
        print('1.php?prec_no=', end="")
        print(f"\033[1;32m{URL_match.string[URL_match.start(2):URL_match.end(2)]}\033[0m", end="")
        print('&block_no=', end="")
        print(f"\033[1;34m{URL_match.string[URL_match.start(3):URL_match.end(3)]}\033[0m", end="")
        print('&year=2024&month=3&day=9&view=')
    print('')
    
    # Retrieve the URLs to the 61 regional maps
    # HTTP request to the starting map
    response_japan_map = requests.get(url_japan_map)

    # Parse the contents of the Response object (initial HTML parsing)
    soup_japan_map = BeautifulSoup(response_japan_map.content, 'html.parser')

    # Pause just to make sure we don't rush things
    print('Pausing after the requests.get() on the starting map interface URL')
    time.sleep(30)

    # Take out just the `area` tags, nested within the `map` tag
    areas_japan_map = soup_japan_map.find('map').find_all('area')

    # Empty list to store all the regional URLs
    jma_regional_url_list = []

    # Work through the list of area tags to extract the href links
    for area_tag in areas_japan_map:
        href = area_tag.get('href')

        # Add on the base URL to get a full URL
        href = 'https://www.data.jma.go.jp/stats/etrn/select/' + href

        # Add the full URL to the list
        jma_regional_url_list.append(href)
    
    # Print statement to notify where we are    
    print(f'Retrieved {len(jma_regional_url_list)} regional map URLs\n')

    # Check if the file exists
    print(f"Python is currently looking here: {Path(fileName).resolve()}")
    if Path(fileName).exists():
        print("JSON file containing final nested dictionary already exists. \nSkip the algorithmic site crawling process. \nDelete `amedas_prec_block_no_dict.json` file in data subfolder if you would like to run the web crawling process.")

        # Open and load the JSON file containing the 
        with open(fileName, 'r', encoding='utf-8') as file:
            prec_block_as_dict = json.load(file)
    else:
        print('Starting algorithmic web crawling for URL identifier discovery')
        # Final nested dictionary
        prec_block_as_dict = {}

        # Regular expressions for finding prec_no, block_no and a vs s
        re_prec_block = r'prec_no=(\d+)&block_no=(\d+)'
        re_a_s = r'javascript:viewPoint\(\'(.)'

        # For each regional map URL
        for i, url_now in enumerate(jma_regional_url_list):

            # Print current region number
            print(f'\tRegion {i+1} out of {len(jma_regional_url_list)}')

            # Scrape and initial parsing of the regional map
            response = requests.get(url_now)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the <area> tags for each JMA station nested under the <map> tag
            stations_in_region = soup.find('map').find_all('area')

            # Work through each weather station inside the region
            for station_now in stations_in_region:
                
                # The weather station name (in Japanese) is stored as the `alt` attribute
                station_name = station_now.get('alt')

                # `href`` attribute for JMA station containing prec_no and block_no and the `onmouseover` containing a vs s
                href = station_now.get('href')
                onmouseover = station_now.get('onmouseover')

                # We can get prec_no and block_no from the href
                match_href = re.search(re_prec_block, href)
                
                # If we have no URL match
                if match_href == None:
                    #print('No URL match: ', station_name)
                    continue

                # Prec and block numbers
                prec_no = match_href[1]
                block_no = match_href[2]

                # In case we have no onmouseover attribute
                if onmouseover == None:
                    #print('No onmouseover match: ', station_name)
                    a_s = 'neither'
                else:
                    # Find the regular expression for a vs s
                    match_onmouse = re.search(re_a_s, onmouseover)
                    
                    # Whether the station is a or s
                    a_s = match_onmouse[1]
                
                # Assign this to a nested dictionary 
                prec_block_as_dict[station_name] = {'prec_no': prec_no, 'block_no': block_no, 'a or s': a_s}        
            
            # Sleep between requests
            time.sleep(30)

        # Write dictionary to a JSON file
        with open(fileName, "w", encoding='utf-8') as file:
            json.dump(prec_block_as_dict, file, indent=4, ensure_ascii=False)  # indent=4 makes it pretty and human-readable
    

if __name__ == "__main__":
    main()
