# Making Legends for Circle Markers in `folium` Maps

No map is complete without a legend. Learn how to make a matching legend for your `folium` maps with scatter plot like circle markers with the `branca` library using HTML and CSS. 

## Blog Post
[Read the full tutorial here](https://datadrivenmai.com/blog/folium-map-legender-scraping/)

## Project Structure
- `README.md` (you are here)
- `folium-map-legend.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `folium-map-legend.py`
    - Python script containing only the essence of the code from the tutorial with minimal explanation
- `data/`
- `images/`

## The Ins and Outs
### Input 
- `amedas_stations_all.csv` inside the `data/` subfolder containing preprocessed data on all weather stations in Japan

### Output
- `sendai_map_legend.html`, a map containing all the weather stations of the Sendai region with circle markers and a matching legend, inside the `data/` subfolder.

## Project Value

### Motivation

Making a legend in `folium` can be a bit tricky, as there is no built-in method to automatically generate a legend from the items drawn on the map. Even in the [`folium` tutorial, legends were manually generated using HTML](https://python-visualization.github.io/folium/latest/advanced_guide/piechart_icons.html#Legend). 

This GitHub directory contains code to crate a custom legend for `folium` maps with circle markers using HTML.


### Key Skills Demonstrated

- Stylize legend boxes with various colors, opacities, corner radius, drop shadows and borders
- Separate inline and internal CSS for common vs variable properties of elements
- Create local functions to incorporate user-specified input into inline CSS to stylize the legend elements
- Include legend titles
- Insert circle markers as legend entries and modify the marker's size, fill color and opacity, and stroke color

## How to Run
Open the `folium-map-legend.ipynb` notebook and run all cells sequentially, or run the `folium-map-legend.py` python script in one go.

### Requirements for Code to Run
- Python 3 (Verified on 3.14.3)
- Python libraries
    - `pandas`
    - `base64`
    - `folium`
    - `branca`
    - `IPython.display`
- `data/` subfolder to save the final CSV file
