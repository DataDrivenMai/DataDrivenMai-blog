"""
Description: Essential code for making a matching legend for `folium` maps with circle markers by coding in HTML and CSS and using MacroElements in the `branca` library.
"""

# Import libraries
import folium
import pandas as pd
import branca
from dotenv import load_dotenv
import os

# Constants
# File location and file name to open and save
fileName = './data/amedas_stations_all.csv'
save_fileName = './data/sendai_map_legend.html'

# Set a base color for the Sendai jurisdiction
color_sendai = '#F78C6B'

# Macro start and end, and CSS properties to include as internal CSS enclosed in <style> tags
macro_start = '{% macro html(this, kwargs) %}'
macro_end = '{% endmacro %}'
legend_css = """
<style type='text/css'>
.map-legend {
    position: fixed;
    z-index: 9999;
    background-color: rgba(255, 255, 255, 0.9);
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    padding: 10px;
    font-family: Arial, sans-serif;
    font-size: 14px;
}
.legend-title {
    font-weight: bold;
    margin-bottom: 8px;
}
.legend-labels {
    list-style-type: none;
    margin-bottom: 5px;
}
.legend-labels li span {
    float: left;
    margin-right: 8px;
    margin-top: 3px;
    border-radius: 50%;
}
</style>
"""

# Legend entries as Python dictionaries
marker_1_dict = {
    'description': 'Rainfall',
    'marker_fill': '#90E0EF', 
    'fill_opacity': 0.5,
    'stroke_color': '#90E0EF', 
    'marker_height': '6px', 
    'marker_width': '6px', 
}
marker_2_dict = {
    'description': 'Rainfall, temperature, wind',
    'marker_fill': color_sendai, 
    'fill_opacity': 0.2,
    'stroke_color': color_sendai, 
    'marker_height': '6px', 
    'marker_width': '6px', 
}
marker_3_dict = {
    'description': 'Rainfall, temperature, wind, relative humidity',
    'marker_fill': color_sendai, 
    'fill_opacity': 0.4,
    'stroke_color': color_sendai, 
    'marker_height': '9px', 
    'marker_width': '9px', 
}
marker_4_dict = {
    'description': 'Rainfall, temperature, wind, relative humidity, sunshine, atmospheric pressure',
    'marker_fill': color_sendai, 
    'fill_opacity': 0.8,
    'stroke_color': color_sendai, 
    'marker_height': '15px', 
    'marker_width': '15px', 
}
marker_5_dict = {
    'description': 'Snowfall',
    'marker_fill': '#FFFFFF', 
    'fill_opacity': 0.5,
    'stroke_color': '#495057', 
    'marker_height': '9px', 
    'marker_width': '9px', 
}
# Integrate the dictionaries above into the dictionary that stores the CSS properties of the legend
legend_dict = {
    'id': 'map-legend', 
    'title': 'Types of Data Collected',
    'bottom': '20px', 
    'right': '20px', 
    'box_width': '250px', 
    'box_height': 'auto', 
    'entries': [marker_1_dict, marker_2_dict, marker_3_dict, marker_4_dict, marker_5_dict]
    }
    
# Local functions
def MapSendaiJurisdiction_popup(sendai_df, mid_lat, mid_long, tile_url, attr):
    """Function to generate the folium map (m) for the Sendai jurisdiction with popups
    AUTHOR:     Mai Tanaka (www.DataDrivenMai.com)
    DATE:       2026-08-24
    REQUIRES: sendai_df = DataFrame containing weather station information from Sendai region
              mid_lat = Latitude to center the map upon
              mid_long = Longitude to center the map upon 
              tile_url = URL for accessing the basemap 
              attr = Attrition for the map data
    PROMISES: m = folium map object of the Sendai jurisdiction, complete with popups
    """

    # Generate a folium map
    m = folium.Map(location=[mid_lat, mid_long], 
                tiles=tile_url, 
                zoom_start=6, 
                min_zoom=5, 
                attr=attr,
                )
    
    # Work through each row to plot a circle marker and generate popups 
    for rowNow in sendai_df.itertuples():
        # Location of the weather station
        lat_now = float(rowNow.latitude_decimal)
        long_now = float(rowNow.longitude_decimal)

        # Make the mouse over information
        mouseover_info = f"<h5>{rowNow.romaji_name.capitalize()} ({rowNow.station_name})</h5>"

        # Make the popup information
        html_popup = GenerateHTML4Popup(rowNow)

        # Adjust size of marker and fill opacity according to station type
        if rowNow.station_type == '雨' or rowNow.station_type == '雪':
            radius_now = 2
            fill_opacity = 0.5
        elif rowNow.station_type == '三':
            radius_now = 2
            fill_opacity = 0.2
        elif rowNow.station_type == '四':
            radius_now = 3
            fill_opacity = 0.4
        elif rowNow.station_type == '官':
            radius_now = 5
            fill_opacity = 0.8

        # Adjust marker fill and stroke colors
        color_sendai = '#F78C6B'
        if rowNow.snowfall_YN == 'Y':
            stroke_color = '#495057'
            if rowNow.station_type == '雪':
                fill_color = 'white'
            else:
                fill_color = color_sendai
        elif rowNow.station_type == '雨':
            fill_color = '#90E0EF'
            stroke_color = '#90E0EF'
        else:
            fill_color = color_sendai
            stroke_color = color_sendai
        
        # Make the marker and add it to the folium map
        markerNow = folium.CircleMarker(
            location=[lat_now, long_now], 
            tooltip=mouseover_info, 
            popup=folium.Popup(     # Insert pop up text
                html=html_popup,
                max_width=300, 
                max_height=150),    
            radius=radius_now,
            weight=2,
            color=stroke_color,
            opacity=1.0,
            fill_color=fill_color,
            fill_opacity=fill_opacity, 
            ).add_to(m)

    # Return the map
    return m

def GenerateHTML4Popup(arg_df_row):
    """Function to generate the HTML to insert into a popup in folium
    AUTHOR:     Mai Tanaka (www.DataDrivenMai.com)
    DATE:       2026-06-30
    REQUIRES: arg_df_row = pandas dataframe row as .itertuples()
    PROMISES: html_popup = html format to pass onto folium html input in popups
    """
    # Determine the color of the Y/N fonts for the data collected
    data_YN = [arg_df_row.rainfall_YN, 
               arg_df_row.temperature_YN, 
               arg_df_row.wind_YN, 
               arg_df_row.sunshine_YN, 
               arg_df_row.relative_humidity_YN, 
               arg_df_row.atmospheric_pressure_YN,
               arg_df_row.snowfall_YN]
    color_YN = []
    for data_YN_now in data_YN:
        if data_YN_now == 'Y':
            color_YN.append('green')
        else:
            color_YN.append('red')
    
    # Make the html_popup (contains a table of meteorological data collected)
    html_popup = f"""
    <h3> {arg_df_row.romaji_name.capitalize()}({arg_df_row.station_name})</h3>
    prec_no: {arg_df_row.prec_no}
    <br>
    block_no: {arg_df_row.block_no}
    <br>
    a or s: {arg_df_row.url_station_type}
    <br>
    Location: {arg_df_row.latitude_decimal:.2f}°, {arg_df_row.longitude_decimal:.2f}°
    <br>
    Elevation: {arg_df_row.elevation} m
    <br>
    <br>    
    <h4>Data Collected</h4>
    <table border="1">
        <tr>
            <td>rainfall</td>
            <td><span style="color: {color_YN[0]}; font-weight: bold;">{data_YN[0]}</span></td>
        </tr>
        <tr>
            <td>temperature</td>
            <td><span style="color: {color_YN[1]}; font-weight: bold;">{data_YN[1]}</span></td>
        </tr>
        <tr>
            <td>wind direction/speed</td>
            <td><span style="color: {color_YN[2]}; font-weight: bold;">{data_YN[2]}</span></td>
        </tr>
        <tr>
            <td>sunshine</td>
            <td><span style="color: {color_YN[3]}; font-weight: bold;">{data_YN[3]}</span></td>
        </tr>
        <tr>
            <td>relative humidity</td>
            <td><span style="color: {color_YN[4]}; font-weight: bold;">{data_YN[4]}</span></td>
        </tr>
        <tr>
            <td>atmospheric pressure</td>
            <td><span style="color: {color_YN[5]}; font-weight: bold;">{data_YN[5]}</span></td>
        </tr>
        <tr>
            <td>snowfall</td>
            <td><span style="color: {color_YN[6]}; font-weight: bold;">{data_YN[6]}</span></td>
        </tr>
    </table>
    <br>
    Thermometer height: {arg_df_row.thermometer_height} m
    <br>
    Anemometer height: {arg_df_row.anemometer_height} m
    <br>
    <br>
    <h4>Observation Start Dates</h4>
    Rain: {arg_df_row.observation_start_date_rain}
    <br>
    Other: {arg_df_row.observation_start_date_other}
    """   
    
    return html_popup

def ColorHex2RGB(hex_str):
    """Function to convert the hexadecimal color to RGB notation
    AUTHOR:     Mai Tanaka (www.DataDrivenMai.com)
    DATE:       2026-06-30
    REQUIRES:   hex_str = hexadecimal notation of the color (eg. '#06D6A0')
    RETURNS:    rgb_val = RGB values in a list (eg. [6, 214, 160])
    """
    # Remove the hash symbol 
    hex_str = hex_str.lstrip('#')
    
    # Convert hex pairs to integers
    rgb_val = []
    for i in (0, 2, 4):
        rgb_val.append(int(hex_str[i:i+2], 16))
        
    return rgb_val

def GenerateLegendHTML(dict_legend):
    """Function to generate the HTML for stylized legend boxes with a legend title and circle markers
    AUTHOR:     Mai Tanaka (www.DataDrivenMai.com)
    DATE:       2026-09-08
    REQUIRES: dict_legend = dictionary containing legend id and CSS properties and values including marker visuals in a nested dictionary
    PROMISES: legend_html = string containing HTML and inline CSS for generating stylized legend with markers
    """
    
    # Check the position of the legend key
    if 'bottom' in dict_legend:
        bottom_pos = dict_legend['bottom']
        top_pos = 'auto'
    elif 'top' in dict_legend:
        top_pos = dict_legend['top']
        bottom_pos = 'auto'
    if 'left' in dict_legend:
        left_pos = dict_legend['left']
        right_pos = 'auto'
    elif 'right' in dict_legend:
        right_pos = dict_legend['right']
        left_pos = 'auto'

    # Add on the new legend HTML legend to the exsiting HTML
    legend_html = f"""
        <div id='{dict_legend['id']}'
            class='map-legend'
            style='
                position: fixed; 
                bottom: {bottom_pos};
                top: {top_pos};
                right: {right_pos};
                left: {left_pos};
                width: {dict_legend['box_width']};
                height: {dict_legend['box_height']}
            '>
            <div class='legend-title'>{dict_legend['title']}</div>
            <div>
                <ul class='legend-labels'>
    """
    # Enter the HTML up to the start of the unordered list

    # Create each legend entry
    for entry_now in dict_legend['entries']:

        # Convert the stroke and fill colors from hex to rgb 
        rgb_fill = str(ColorHex2RGB(entry_now['marker_fill']))
        rgb_str = str(ColorHex2RGB(entry_now['stroke_color']))

        # Take out the parenthesis and add the alpha or opacity
        fill_rgba = rgb_fill[1:-1] + ', ' + str(entry_now['fill_opacity'])
        stroke_rgba = rgb_str[1:-1] + ', 1.0' # Stroke opacity is always 100 %

        # Make the appropriate HTML for the legend entry
        marker_html = f"""
                    <li><span 
                        style='
                            height: {entry_now['marker_height']};
                            width: {entry_now['marker_width']};
                            background: rgba({fill_rgba});
                            border: 2px solid rgba({stroke_rgba});
                        '></span>
                        {entry_now['description']}
                    </li>                    
        """

        # Add on the marker_html to the legend_html
        legend_html += marker_html

    # Concatenate the closing HTML tags for the unordered list, the <div> containing the unordered list, and the <div> for the legend box
    legend_html += """
                </ul>
            </div>
        </div>
    """

    return legend_html




# Main script
def main():
    """Main script that draws the map of Sendai and saves the HTML."""

    # Import .env file containing the API key for CARTO ('carto_API_key')
    if load_dotenv():
        # CARTO API key (request one free at https://carto.com/basemaps/apikey)
        carto_api_key = os.getenv('carto_API_key')

        # Construct the tile URL template with the API key parameter
        tile_url = f"https://basemaps.cartocdn.com/rastertiles/light_all/{{z}}/{{x}}/{{y}}.png?key={carto_api_key}"

        # Manual attrition needed 
        attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    else:
        # If no .env file, use open street map
        tile_url = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

        # Attrition
        attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        
    # Read the CSV file containing all information
    amedas_df_all = pd.read_csv(fileName, encoding='utf-8')

    # Getting rid of the columns we won't be using
    amedas_df = amedas_df_all.drop(["prefectural_bureau", 
                                    "station_id", 
                                    "katakana_name", 
                                    "location", 
                                    "observation_start_date", 
                                    "weather_info_name", 
                                    "notes1", 
                                    "notes2"], axis=1)

    # Using only the rows in the Sendai region
    boolMask = (amedas_df['prec_no'] >= 31) & (amedas_df['prec_no'] <= 36)
    sendai_df = amedas_df[boolMask].reset_index(drop=True)

    # Find the middle of the map
    mid_lat = sendai_df['latitude_decimal'].mean()
    mid_long = sendai_df['longitude_decimal'].mean()

    # Create the map with the complete pop up text
    m = MapSendaiJurisdiction_popup(sendai_df, mid_lat, mid_long, tile_url, attr)
    
    # Create legend_html using the legend_dict and concatenate it all
    legend_html = GenerateLegendHTML(legend_dict)
    legend_html_all = macro_start + legend_css + legend_html + macro_end

    # Create a branca macroelement object and overwrite it with our legend html
    legend = branca.element.MacroElement()
    legend._template = branca.element.Template(legend_html_all)

    # Add the legend to the map 
    m.get_root().add_child(legend)

    # Save the file
    m.save(save_fileName)

        
if __name__ == "__main__":
    main()
