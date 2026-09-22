# Mapping Scatter Plots on Folium Maps with `folium.CircleMarker()`

How to make scatter plot like circle markers on `folium` maps. 

## Blog Post
[Read the full tutorial here](https://datadrivenmai.com/blog/folium-map-scatter-plot/)

## Project Structure
- `README.md` (you are here)
- `folium-map-scatter-plot.ipynb`
    - Step-by-step tutorial identical to the original blog post
- `folium-map-scatter-plot.py`
    - Python script containing only the essence of the code from the tutorial with minimal explanation
- `data/`
- `images/`

## The Ins and Outs
### Input 
- `amedas_stations_all.csv` inside the `data/` subfolder containing preprocessed data on all weather stations in Japan

### Output
- `sendai_map_scatter_plot.html`, a map containing all the weather stations of the Sendai region with appropriately set marker colors and opacities, hover over text and pop up text, is saved inside the `data/` subfolder

## Project Value

### Motivation
Maps using the reverse-teardrop shaped marker in folium can quickly become congested and difficult to navigate. This tutorial shows how to use `folium.CircleMarker()` object to generate simple scatter plot like maps, complete with hover over and pop up text. 

### Key Skills Demonstrated

- Mark locations on a map using `folium.CircleMarker()`
    - Modify the marker's fill and stroke color
    - Adjust the marker's opacity
- Add mouse-over text, which appears when the cursor hovers over the marker, using HTML 
- Add pop up text, which appears when the user clicks the marker, using HTML 

## How to Run
Open the `folium-map-scatter-plot.ipynb` notebook and run all cells sequentially, or run the `folium-map-scatter-plot.py` python script in one go.

### Requirements for Code to Run
- Python 3 (Verified on 3.14.3)
- Python libraries
    - `pandas`
    - `folium`
    - `base64`
    - `IPython.display`
    - `dotenv`
    - `os`
- `data/` subfolder to load the `amedas_stations_all.csv` file and save the `sendai_map_scatter_plot.html` map
