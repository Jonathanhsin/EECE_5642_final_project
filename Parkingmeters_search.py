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
        dcc.Input(
            id='my_{}'.format(x),
            type=x,
            placeholder="Insert Street Name",  # A hint to the user of what can be entered in the control
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
    html.Div([
            dcc.Input(
                id='day_sections',
                type='text',
                placeholder='Enter Day',
                debounce=True,           # changes to input are sent to Dash server only on enter or losing focus
                pattern=r"^[A-Za-z].*",  # Regex: string must start with letters only
                spellCheck=True,
                name='text',             # the name of the control, which is submitted with the form data
                list='browser',          # identifies a list of pre-defined options to suggest to the user
                n_submit=0,              # number of times the Enter key was pressed while the input had focus
                n_submit_timestamp=-1,   # last time that Enter was pressed
                autoFocus=True,          # the element should be automatically focused after the page loaded
                n_blur=0,                # number of times the input lost focus
                n_blur_timestamp=-1,     # last time the input lost focus.
                # selectionDirection='', # the direction in which selection occurred
                # selectionStart='',     # the offset into the element's text content of the first selected character
                # selectionEnd='',       # the offset into the element's text content of the last selected character
            ),
        ]),

    html.Br(),
    html.Datalist(id='browser', children=[
        html.Option(value="Monday-Saturday"),
        html.Option(value="Sunday"),

    ]),

    html.Br(),
    dcc.Graph(id="mymap"),
])


@app.callback(
    Output(component_id='mymap', component_property='figure'),
    [Input(component_id='my_{}'.format(x), component_property='value')
     for x in input_types
     ],
    Input(component_id='day_sections', component_property='value'),
)
def update_graph(blk_name, day_section):
    print("text: " + str(blk_name))
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

