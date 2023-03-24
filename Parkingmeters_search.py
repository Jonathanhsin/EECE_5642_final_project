import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

# read the data from string
# Import and filter data into pandas data frame
df = pd.read_csv("Parking_Meters.csv")

Street_list = np.append('ALL_BLK', df['BLK_NO'].unique())
visible = Street_list
input_types = ['text']

# Creating lists for times
pay_policy = df['PAY_POLICY']
pay_times = []

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
        dcc.Input(
            id='my_{}'.format(x),
            type=x,
            placeholder="insert text",  # A hint to the user of what can be entered in the control
            debounce=True,  # Changes to input are sent to Dash server only on enter or losing focus
            minLength=0, maxLength=50,  # Ranges for character length inside input box
            autoComplete='on',
            disabled=False,  # Disable input box
            readOnly=False,  # Make input box read only
            required=False,  # Require user to insert something into input box
            size="20",  # Number of characters that will be visible inside box
            # style={'':''}                     # Define styles for dropdown (Dropdown video: 13:05)
            # className='',                     # Define style from separate CSS document (Dropdown video: 13:05)
            # persistence='',                   # Stores user's dropdown changes in memory (Dropdown video: 16:20)
            # persistence_type='',              # Stores user's dropdown changes in memory (Dropdown video: 16:20)
        ) for x in input_types
    ]),

    html.Br(),
    dcc.Graph(id="mymap"),
])

@app.callback(
    Output(component_id='mymap', component_property='figure'),
    [Input(component_id='my_{}'.format(x), component_property='value')
     for x in input_types
     ],
)

def update_graph(blk_name):
    print("text: " + str(blk_name))
    if blk_name is None or blk_name not in Street_list:
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
        filtered_df = df[df['BLK_NO'] == blk_name]
        boston_map = px.scatter_mapbox(
            filtered_df,
            lat=filtered_df['LATITUDE'],
            lon=filtered_df['LONGITUDE'],
            zoom=17,
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