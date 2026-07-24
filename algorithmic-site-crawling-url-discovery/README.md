# Algorithmic Site Crawling for Automatic Discovery of URL Identifiers of Japan's Weather Stations

This folder contains information and code demonstrating the process of algorithmically crawling the Japan Meteorological Agency (JMA) website to automatically discover the unique identifiers for each weather station in Japan. The unique identifiers are stored as a nested dictionary and saved as a JSON file, which can be used in later scripts to generate the URLs associated with each weather station. 

## Blog Post
[Read the full tutorial here](https://datadrivenmai.com/blog/algorithmic-site-crawling-url-discovery/)

## Project Structure
- `README.md` (you are here)
- `algorithmic-site-crawling-url-discovery.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `algorithmic-site-crawling-url-discovery.py`
    - Python script containing only the essential code from the tutorial with minimal explanation
- `data/`
- `images/`

## The Ins and Outs
### Input 
- The starting map interface URL: `url_japan_map = 'https://www.data.jma.go.jp/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view='`
    - Note that the code is suited for the JMA website and its unique map interface design. If you want to crawl a different site, you will need to use the code in parts and modify the tags and attributes that you search for.

### Output
- `data/amedas_prec_block_no_dict.json` file of the nested python dictionary containing the unique identifiers for each weather station
    - Note that the weather station name is stored in Japanese

## Project Value

### Motivation
Copying and pasting several webpages to scrape data from can be an error prone process, especially when you have many URLs. You may miss a URL, accidently include duplicate URLs, or introduce a typo into the URL resulting in a failure to scrape data. For webpages all residing in the same website, you can automatically discover the desired URLs with algorithmic site crawling.

### Key Skills Demonstrated

- From a starting JMA map interface URL, scrape the HTML to collect `href` attributes to generate complete URLs to each regional map using `requests` and `Beautiful Soup` libraries
- From each regional map URL, scraped and parse `href` and `onmouseover` attributes which contain the three unique identifiers for each JMA weather station
- Use regular expressions (regex) to extract identifiers unique to each JMA weather station
- Stored the identifiers as a nested dictionary for all JMA weather stations and saved it as a JSON file

## How to Run
If you would like the code to do the web crawling process (which will take just over 30 minutes), please ensure that you **delete the `amedas_prec_block_no_dict.json` file in the `data/` subfolder**. Then, open the `algorithmic-site-crawling-url-discovery.ipynb` notebook and run all cells sequentially, or run the `algorithmic-site-crawling-url-discovery.py` python script in one go.

### Requirements for Code to Run
- Python 3 (Verified on 3.14.3)
- Python libraries
    - `re`
    - `requests`
    - `bs4`
    - `time`
    - `pathlib`
    - `json`
- `data/` subfolder to save `amedas_prec_block_no_dict.json` file containing the nested dictionary
