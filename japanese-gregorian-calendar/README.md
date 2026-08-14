# Conversion of Japanese Dates into the Gregorian Calendar

This project demonstrates the conversion of Japanese dates into their Gregorian calendar equivalents with Python, using real data downloaded from the Japan Meteorological Agency (JMA) website.

## Blog Post
[Read the full tutorial here](https://datadrivenmai.com/blog/japanese-gregorian-calendar/index.html)

## Project Structure
- `README.md` (you are here)
- `japanese-gregorian-calendar.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `japanese-gregorian-calendar.py`
    - Python script containing only the essence of the code from the tutorial with minimal explanation
- `data/`

## The Ins and Outs
### Input 
- Demo CSV file `ame_master_20260324.csv` containing real Japanese dates in one of their columns

### Output
- `data/japanese_gregorian_calendar_python.csv` file is saved after running the python file, while `data/japanese_gregorian_calendar_jupyter.csv` file is saved after running the Jupyter file. Data columns in each output file:
    - Original string of Japanese dates
    - Converted Gregorian date equivalent to the start of rainfall data collection
    - Gregorian date equivalent to the start of all other weather data collection

## Project Value

### Motivation

Data collected by the Japanese government and other official entities often rely on the Japanese calendar system, which starts a new era aperiodically. Being able to convert the Japanese dates into their Gregorian calendar equivalent is useful as it allows data to be visualized on a continuum, and can easily be integrated with other data from non-Japanese sources. 

### Key Skills Demonstrated
- Used regular expressions (regex) to find and parse the era name, year number, month and day from real data
- Improved the regular expressions to work with exceptions in the data, which may be caused by human error
- Converted Japanese years into Gregorian years by simple addition of the Japanese years to the "year 0" for the era in question

## How to Run
Open the `japanese-gregorian-calendar.ipynb` notebook and run all cells sequentially, or run the `japanese-gregorian-calendar.py` python script in one go.

### Requirements for Code to Run
- Python 3 (Verified on 3.14.3)
- Python libraries
    - `pandas`
    - `re`
- `data/` subfolder to read and save CSV files
