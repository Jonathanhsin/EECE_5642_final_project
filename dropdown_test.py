import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output

app = dash.Dash(__name__)

# read the data from string
# Import and filter data into pandas data frame
df = pd.read_csv("Parking_Meters.csv")

Street_list = np.append('ALL_BLK', df['BLK_NO'].unique())
visible = Street_list
day_options = ['Monday-Saturday', 'Sunday']
input_types = ['text']

# Creating lists for times
pay_policy = df['PAY_POLICY']
pay_times = []

# Creating lists for streets
orig_names = df['STREET']
print(orig_names[1])
street_names = []
for i in range(0, len(orig_names)):
    street_names.append((orig_names[i].split(" ST")[0]).split(" RD")[0])
df['STREET_NAMES'] = street_names
street_names = [*set(street_names)]

for times in pay_policy:
    just_the_time = times.split(" ")
    pay_times.append(just_the_time[0])


# returns the meter information for the given index
def getMeter(index):
    return df.iloc[[index]]


# return if the meter at given index is paid at the given int time (morning = AM boolean)
def meterPaid(index, time, morning):
    if morning:
        if time >= int(pay_times[index][0:2]):
            return True
    else:
        if time <= int(pay_times[index][8:10]):
            return True
    return False


# return boolean list of if the meters are paid at the given int time (morning = AM boolean)
def meterPaidList(time, morning):
    paidBool = []
    for tm in pay_times:
        appended = False
        if morning:
            if time >= int(tm[0:2]):
                paidBool.append(True)
                appended = True
        else:
            if time <= int(tm[8:10]):
                paidBool.append(True)
                appended = True
        if not appended:
            paidBool.append(False)

    return paidBool


app.layout = html.Div([
    html.Div([
        dcc.Dropdown(street_names, placeholder='Select a Street', id='street_sections'),
    ]),

    html.Br(),
    html.Div([
            dcc.Dropdown(['Monday-Saturday', 'Sunday'], placeholder='Select a Day', id='day_sections'),
        ]),


    html.Br(),
    html.Div([
            dcc.Dropdown(['8:00 AM - 8:00 PM', '8:00 PM - 12:00 AM', '12:00 AM - 8:00 AM'], placeholder='Select an Hour', id='hour_sections'),
        ]),
    html.Br(),
    dcc.Graph(id="mymap"),
])

@app.callback(
    Output(component_id='mymap', component_property='figure'),
    Input(component_id='street_sections', component_property='value'),
    Input(component_id='day_sections', component_property='value'),
    Input(component_id='hour_sections', component_property='value'),
)

def update_graph(blk_name, day_value, hour_value):
    print("text: " + str(blk_name))
    print("day: " + str(day_value))
    print("hour: " + str(hour_value))
    if blk_name is None or blk_name.upper() not in street_names:
        filtered_df = df.copy()
        boston_map = px.scatter_mapbox(
            filtered_df,
            lat=filtered_df['LATITUDE'],
            lon=filtered_df['LONGITUDE'],
            hover_name=filtered_df['STREET'],
            zoom=13,
            custom_data=['STREET', 'LATITUDE', 'LONGITUDE', 'PAY_POLICY']
        )
        boston_map.update_traces(marker=dict(size=5, color="green"))
    else:
        print(blk_name.upper())
        filtered_df = df[df["STREET_NAMES"] == blk_name.upper()]
        # temp additional zoom determined via number of locations
        # can maybe try calculating distance between meters
        if len(filtered_df) < 5:
            boston_map = px.scatter_mapbox(
                filtered_df,
                lat=filtered_df['LATITUDE'],
                lon=filtered_df['LONGITUDE'],
                zoom=16,
                custom_data=['STREET', 'LATITUDE', 'LONGITUDE', 'PAY_POLICY']
            )
            boston_map.update_traces(marker=dict(size=10, color="green"))
        else:

            boston_map = px.scatter_mapbox(
                filtered_df,
                lat=filtered_df['LATITUDE'],
                lon=filtered_df['LONGITUDE'],
                zoom=15.5,
                custom_data=['STREET', 'LATITUDE', 'LONGITUDE', 'PAY_POLICY']
            )
            boston_map.update_traces(marker=dict(size=10, color="green"))

    boston_map.update_layout(mapbox_style="open-street-map")
    boston_map.update_layout(height=900, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    boston_map.update_traces(
        hovertemplate="<br>".join([
            "Street: %{customdata[0]}",
            "Latitude: %{customdata[1]}",
            "Longitude: %{customdata[2]}",
            "Pay Period: %{customdata[3]}",
        ]))
    return boston_map


if __name__ == '__main__':
    app.run_server(debug=True)
