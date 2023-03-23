import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
app = dash.Dash(__name__)

# read the data from string
# Import and filter data into pandas data frame
df = pd.read_csv("Parking_Meters.csv")

Street_list = np.append('ALL_STREET', df['STREET'].unique())
visible = Street_list
input_types = ['text']
base_case = True

app.layout = html.Div([
    html.Div([
        dcc.Input(
            id='my_{}'.format(x),
            type=x,
            placeholder="insert block ID",  # A hint to the user of what can be entered in the control
            debounce=True,                      # Changes to input are sent to Dash server only on enter or losing focus
            minLength=0, maxLength=50,          # Ranges for character length inside input box
            autoComplete='on',
            disabled=False,                     # Disable input box
            readOnly=False,                     # Make input box read only
            required=False,                     # Require user to insert something into input box
            size="20",                          # Number of characters that will be visible inside box
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



def update_graph(street_name):
    print("text: " + str(street_name))

    if (street_name == None):
        filtered_df = df.copy()
    else:
        temp = [v for v in df['STREET'] if v.startswith(street_name)]

    boston_map = px.scatter_mapbox(
        filtered_df,
        lat=filtered_df['LATITUDE'],
        lon=filtered_df['LONGITUDE'],
        hover_name=filtered_df['STREET'],
        zoom=13
    )
    boston_map.update_layout(mapbox_style="open-street-map")
    boston_map.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})
    boston_map.update_traces(marker=dict(size=5, color="red"))
    return (boston_map)

if __name__ == '__main__':
    app.run_server(debug=True)