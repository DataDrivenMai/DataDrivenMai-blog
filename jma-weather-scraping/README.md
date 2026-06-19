# JMA Weather Data Scraping and Parsing

This project demonstrates how to scrape, parse, structure and save weather data (per 10 min) from the Japan Meteorological Agency (JMA) website using Python.

## Blog Post
[Read the full tutorial here](https://www.DataDrivenMai/blog/jma-weather-scraping/)

## Project Structure
- `README.md` (you are here)
- `jma-weather-scraping.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `jma-weather-scraping.py`
    - Python script containing only the essence of the code from the tutorial with minimal explanation
- `data/`
- `images/`

## The Ins and Outs
### Input 
- URL to weather data collected every 10 min from one s1 type JMA observation site
    - Default URL provided (Tokyo site for March 9, 2024)

### Output
-  `jma_weather_scraping_xxx.csv` with 10 min weather data, ready for further analysis
    - `_xxx.csv` is `_jupyter.csv` when `jma_weather_scraping.ipynb` file is ran
    - `_xxx.csv` is `_python.csv` when `jma_weather_scraping.py` file is ran

## Project Value

### Motivation
Access to structured weather data is essential for time-series analysis and modeling, but some JMA data are only available through HTML tables. 
This project builds a pipeline to extract and clean that data for analysis.

### Key Skills Demonstrated
- Scraping tabular data using `requests`
- Parsing HTML with `BeautifulSoup`
- Converting simple timestamps into useful `datetime` objects
- Attaching time zone information to `datetime` objects with `pytz`
- Cleaning and exporting data using `pandas`

## How to Run
Open the `jma-weather-scraping.ipynb` notebook and run all cells sequentially, or run the `jma-weather-scraping.py` python script in one go.

### Requirements for Code to Run
- Python 3.x
- Python libraries
    - `requests`
    - `bs4`
    - `datetime`
    - `pytz`
    - `pandas`
- `data/` subfolder to save the final CSV file
