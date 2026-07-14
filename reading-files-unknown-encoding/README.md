# Reading Files of Unknown Encoding

This folder contains information and code on reading in CSV files with unknown encoding into `pandas` DataFrames.

## Blog Post
[Read the full tutorial here](https://datadrivenmai.com/blog/reading-files-unknown-encoding/)

## Project Structure
- `README.md` (you are here)
- `reading-files-unknown-encoding.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `reading-files-unknown-encoding.py`
    - Python script containing only the essential code from the tutorial with minimal explanation
- `data/`

## The Ins and Outs
### Input 
- Demo CSV file `ame_master_20260324.csv` with unknown encoding

### Output
- `data/ame_master_utf8.csv` file is saved with the python file, `reading-files-unknown-encoding.py`, but not with the Jupyter notebook.

## Project Value

### Motivation
Manually testing all possible encoding models to open a mystery CSV file with unknown encoding is inefficient. An adaptable procedure that can be applied to any file of unknown encoding is desired.

### Key Skills Demonstrated

- Open a mystery CSV file as raw binary data using `'rb'` designation on the `open()` function
- Detect the encoding of the mystery CSV file by using `charset_normalizer.detect()` on the raw binary data
- Use the detected encoding to read the mystery CSV file as a `pandas` DataFrame

## How to Run
Open the `reading-files-unknown-encoding.ipynb` notebook and run all cells sequentially, or run the `reading-files-unknown-encoding.py` python script in one go.

### Requirements for Code to Run
- Python 3 (Verified on 3.14.3)
- Python libraries
    - `charset_normalizer`
	- `pandas`
- `data/` subfolder to load `ame_master_20260324.csv` file and save the UTF-8 version in the Python script
