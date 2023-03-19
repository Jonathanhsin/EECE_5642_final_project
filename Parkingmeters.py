import plotly.graph_objects as go
import numpy as np
import pandas as pd


# read the data from string
parking_meters = pd.read_csv("Parking_Meters.csv")

# empty traces and buttons list
# current buttons are stored in non searchable drop down
# want to convert to searchable via https://plotly.com/python/figurewidget-app/

traces = []
buttons = []
# storing by blocks for now
BLK_list = np.append('All_BLK', parking_meters['BLK_NO'].unique())
visible = BLK_list
for BLK in BLK_list:

    if BLK == 'All_BLK':
        # stores a copy for entire view
        filtered_df = parking_meters.copy()
    else:
        # filters out meters per unique block
        filtered_df = parking_meters[parking_meters['BLK_NO'] == BLK]
    # add to traces
    traces.append(go.Scattermapbox(
        lat=filtered_df['LATITUDE'],
        lon=filtered_df['LONGITUDE'],
        mode='markers',
        visible=True if BLK == BLK_list[0] else False,
        customdata=filtered_df,
        text=filtered_df['STREET'],
        hoverinfo='text',
        marker=go.scattermapbox.Marker(
            size=5,
            color='rgb(255, 0, 0)',
            opacity=1
        )
    ))
    # add button to drop down
    buttons.append(
        dict(
            method='update',
            label=BLK,
            args=[{'visible': list(visible == BLK)}], )
    )

# create figure
fig = go.Figure(data=traces)

# add buttons
fig.update_layout(
    mapbox=dict(
        style='open-street-map',
        bearing=0,
        # center the map
        center=go.layout.mapbox.Center(
            lat=parking_meters['LATITUDE'].mean(),
            lon=parking_meters['LONGITUDE'].mean(),
        ),
        # zoom ranges from 0-20
        zoom=13
    ),
    margin={'r':10, 't': 0, 'l': 0, 'b': 0}
)

# add buttons
fig.update_layout(
    height=1000,
    showlegend=False,
    updatemenus=[
        dict(
            buttons=buttons,
            direction='down',
            x=0.05,
            y=1.0,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=8),
        ),
    ]
)
fig.show()


"""
# working basic plot of parking meters in boston
fig = go.Figure()
fig.add_trace(go.Scattermapbox(
                lat=parking_meters['LATITUDE'],
                lon=parking_meters['LONGITUDE'],
                marker=go.scattermapbox.Marker(
                    size=5,
                    color='rgb(255, 0, 0)',
                    opacity = 1
                ),
                text=parking_meters['STREET'],
                hoverinfo='text'
            ))
fig.update_layout(
    mapbox=dict(
        style='open-street-map',
        #accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=parking_meters['LATITUDE'].mean(),
            lon=parking_meters['LONGITUDE'].mean(),
        ),
        zoom=13
    ),
    margin={'r':10, 't': 0, 'l': 0, 'b': 0}
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(title="Parking Meters")
fig.show()
"""

