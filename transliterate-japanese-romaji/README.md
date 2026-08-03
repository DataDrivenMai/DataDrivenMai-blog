# Transliteration of Japanese Hiragana and Katakana Using the Roman Alphabet

This projects demonstrates how to transliterate Japanese words written in hiragana or katakana into the Roman alphabet using `jaconv` or `pykakasi` Python libraries.

## Blog Post
[Read the full tutorial here](https://datadrivenmai.com/blog/transliterate-japanese-romaji/)

## Project Structure
- `README.md` (you are here)
- `transliterate-japanese-romaji.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `transliterate-japanese-romaji.py`
    - Python script containing only the essence of the code from the tutorial with minimal explanation

## The Ins and Outs
### Input 
- Three lists of five relatively well known Japanese words (provided)
    - One list written in hiragana
    - One list written in full-width katakana
    - One list written in half-width katakana

### Output
- Nothing. Just printed outputs to the terminal

## Project Value

### Motivation

Japanese data may contain Japanese letters in the data, which may need to be converted into the English alphabet for readability. This blog post shows how to use the `jaconv` and `pykakasi` libraries to transliterate Japanese words into their romaji equivalent. 

### Key Skills Demonstrated
- Transliterate hiragana into the Roman alphabet using the `jaconv` and the `pykakasi` libraries
- Transliterate katakana into the Roman alphabet using the `jaconv` and `pykakasi` libraries
- Convert hankaku (half-width) katakana into zenkaku (full-width) katakana using `jaconv.hankaku2zenkaku()` before conversion

## How to Run
Open the `transliterate-japanese-romaji.ipynb` notebook and run all cells sequentially, or run the `transliterate-japanese-romaji.py` python script in one go.

### Requirements for Code to Run
- Python 3 (Verified on 3.14.3)
- Python libraries
    - `jaconv`
    - `pykakasi`
