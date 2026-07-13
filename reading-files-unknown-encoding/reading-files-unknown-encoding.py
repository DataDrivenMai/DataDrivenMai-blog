"""
Description: Essential code for reading files of unknown encoding.
"""

# Import libraries
import charset_normalizer
import pandas as pd

# Constants
# CSV file with unknown encoding to open as demonstration
fileName = './data/ame_master_20260324.csv'

# Main script
def main():
    """Main script that reads in the mystery CSV file as raw binary data, detects the encoding model used and uses that encdoing to read in the mystery CSV file as a `pandas` DataFrame."""

    # Step 1: Read file as raw binary data
    with open(fileName, "rb") as f:
        raw_data = f.read()

    # Step 2: Use charset_normalizer to detect the encoding
    detected_data = charset_normalizer.detect(raw_data)
    detected_encoding = detected_data["encoding"]

    # print out the detected encoding
    if detected_data['encoding'] is not None:
        print('Detected encoding: ', detected_encoding)

    # Read the CSV file using the detected encoding
    amedas_df = pd.read_csv(fileName, encoding=detected_encoding)

    # Write out the decoded CSV with UTF-8 encoding
    amedas_df.to_csv('output.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main()
