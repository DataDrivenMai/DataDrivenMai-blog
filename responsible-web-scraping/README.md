# Web Scraping Etiquette

This folder contains information and code demonstrating good web scraping practices.

## Blog Post
[Read the full tutorial here](https://www.DataDrivenMai/blog/responsible-web-scraping)

## Project Structure
- `README.md` (you are here)
- `responsible-web-scraping.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `responsible-web-scraping.py`
    - Python script containing only the essential code from the tutorial with minimal explanation
- `data/`
- `images/`

## The Ins and Outs
### Input 
- URL to read `robots.txt` file from
- One good and one bad URL for demonstration

### Output
- `data/equibase_robots.txt` file is saved with the python file, `responsible-web-scraping.py`, but not with the Jupyter notebook.

## Project Value

### Motivation
Scraping data from websites too quickly can overload the server, slow down or crash the website, and be mistakened as a malicious attack. Good web scraping practices keep you from inadvertently leading a cyberattack on a website, and prevents your IP address from being banned of access. This tutorial will demonstrate how beginners can carry out data scraping in a responsible and robust manner.

### Key Skills Demonstrated
- Read `robots.txt` files to see
	- Which webpages you are and are not allowed to access
	- Determine the minimum time to pause between `requests.get()`
- Pause between HTTP requests using the `time.sleep()` function
- Handle exceptions using `try`, `except` and `else`
	- Specify a `timeout` parameter on the `requests.get()` function 

## How to Run
Open the `responsible-web-scraping.ipynb` notebook and run all cells sequentially, or run the `responsible-web-scraping.py` python script in one go.

### Requirements for Code to Run
- Python 3.x
- Python libraries
    - `urllib`
	- `requests`
	- `time`
	- `pandas`
	- `bs4`
- `data/` subfolder to save the `equibase_robots.txt` file 
