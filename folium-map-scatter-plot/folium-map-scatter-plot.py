"""
Description: Essential code for drawing scatter plot like markers for weather stations in the Sendai region in Japan, complete with hover over and pop up text, using the `folium` library.
"""

# Import libraries
import folium
import pandas as pd

# Constants
# File location and file name to open and save
fileName = './data/amedas_stations_all.csv'
save_fileName = './data/sendai_map_scatter_plot.html'
# Set a base color for the Sendai jurisdiction
color_sendai = '#F78C6B'


# Local functions
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


# Main script
def main():
    """Main script that draws the map of Sendai and saves the HTML."""

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
    
   # Generate a folium map
    m = folium.Map(location=[mid_lat, mid_long], 
                tiles='cartodb positron', 
                zoom_start=6, 
                min_zoom=5)

    # Work through each row to plot a circle marker and generate popups 
    for rowNow in sendai_df.itertuples():
        # Location of the weather station
        lat_now = float(rowNow.latitude_decimal)
        long_now = float(rowNow.longitude_decimal)

        # Make the mouse over information
        mouseover_info = f"<h5>{rowNow.romaji_name.capitalize()}({rowNow.station_name})</h5>"

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
    
    # Save the file
    m.save(save_fileName)


if __name__ == "__main__":
    main()
