import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output

app = dash.Dash(__name__)


def getDayVal(day):
    dayVal = 0
    if day == "Monday" or day.upper() == "MON":
        dayVal = 1
    elif day == "Tuesday" or day.upper() == "TUE":
        dayVal = 2
    elif day == "Wednesday" or day.upper() == "WED":
        dayVal = 3
    elif day == "Thursday" or day.upper() == "THU":
        dayVal = 4
    elif day == "Friday" or day.upper() == "FRI":
        dayVal = 5
    elif day == "Saturday" or day.upper() == "SAT":
        dayVal = 6
    elif day == "Sunday" or day.upper() == "SUN":
        dayVal = 7
    return dayVal


def getHourVal(hour):
    militaryTime = 0
    halfHour = 0

    if hour[5:7] == "PM":
        militaryTime = 12
    if hour[3:5] == "30":
        halfHour = 0.5

    newHour = int(hour[0:2])
    if newHour == 12:
        newHour = 0

    newHour = newHour + militaryTime + halfHour
    return newHour


listOfHours = ['12:00AM-12:29AM', '12:30AM-12:59AM', '01:00AM-01:29AM', '01:30AM-01:59AM',
               '02:00AM-02:29AM', '02:30AM-02:59AM', '03:00AM-03:29AM', '03:30AM-03:59AM',
               '04:00AM-04:29AM', '04:30AM-04:59AM', '05:00AM-05:29AM', '05:30AM-05:59AM',
               '06:00AM-06:29AM', '06:30AM-06:59AM', '07:00AM-07:29AM', '07:30AM-07:59AM',
               '08:00AM-08:29AM', '08:30AM-08:59AM', '09:00AM-09:29AM', '09:30AM-09:59AM',
               '10:00AM-10:29AM', '10:30AM-10:59AM', '11:00AM-11:29AM', '11:30AM-11:59AM',
               '12:00PM-12:29PM', '12:30PM-12:59PM', '01:00PM-01:29PM', '01:30PM-01:59PM',
               '02:00PM-02:29PM', '02:30PM-02:59PM', '03:00PM-03:29PM', '03:30PM-03:59PM',
               '04:00PM-04:29PM', '04:30PM-04:59PM', '05:00PM-05:29PM', '05:30PM-05:59PM',
               '06:00PM-06:29PM', '06:30PM-06:59PM', '07:00PM-07:29PM', '07:30PM-07:59PM',
               '08:00PM-08:29PM', '08:30PM-08:59PM', '09:00PM-09:29PM', '09:30PM-09:59PM',
               '10:00PM-10:29PM', '10:30PM-10:59PM', '11:00PM-11:29PM', '11:30PM-11:59PM']


# read the data from string
# Import and filter data into pandas data frame
df = pd.read_csv("Parking_Meters.csv")

Street_list = np.append('ALL_BLK', df['BLK_NO'].unique())
visible = Street_list
# day_options = ['Monday-Saturday', 'Sunday']
day_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
input_types = ['text']

# Creating lists for times
pay_policy = df['PAY_POLICY']
pay_times = []

# Creating lists for streets
orig_names = df['STREET']
street_names = []
for i in range(0, len(orig_names)):
    street_names.append((orig_names[i].split(" ST")[0]).split(" RD")[0])
df['STREET_NAMES'] = street_names
street_names = [*set(street_names)]

# Creating lists for times and days
start_times = []
end_times = []
start_days = []
end_days = []
normal_cost = []
for pay_vals in pay_policy:
    policy_split = pay_vals.split(" ")
    pay_times.append(policy_split[0])
    start_times.append(int(policy_split[0][0:2]))
    end_times.append(int(policy_split[0][8:10]))
    start_days.append(getDayVal(policy_split[1][0:3]))
    end_days.append(getDayVal(policy_split[1][4:7]))
    normal_cost.append(policy_split[2])

df["END_DAYS"] = end_days
df["PAY_AMOUNT"] = normal_cost

'''
def getCosts(day):
    newCosts = []
    index = 0
    dayVal = getDayVal(day)
    for endDay in df["END_DAYS"]:
        if dayVal > endDay:
            newCosts.append("FREE")
        else:
            newCosts.append(normal_cost[i])
        index = index + 1
    return newCosts
'''


def getCosts(day, hour):
    newCosts = []
    index = -1
    dayVal = getDayVal(day)
    hourVal = getHourVal(hour[0:7])

    for payPolicy in df["PAY_POLICY"]:
        index = index + 1
        policyList = payPolicy.split(", ")
        appended = False
        for policy in policyList:
            splitPolicy = policy.split(" ")
            times = splitPolicy[0]
            days = splitPolicy[1]
            splitDays = days.split("-")

            if splitDays[0] == "SAT":
                if getDayVal(splitDays[0]) == dayVal:
                    if getHourVal(times[8:15]) > hourVal >= getHourVal(times[0:7]):
                        newCosts.append(normal_cost[index])
                        appended = True
            else:
                if getDayVal(splitDays[1]) >= dayVal:
                    if getHourVal(times[8:15]) > hourVal >= getHourVal(times[0:7]):
                        newCosts.append(normal_cost[index])
                        appended = True

        if not appended:
            newCosts.append("FREE")

    return newCosts


'''
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
'''

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(street_names, placeholder='Select a Street', id='street_sections'),
    ]),

    html.Br(),
    html.Div([
            dcc.Dropdown(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                         placeholder='Select a Day', id='day_sections'),
        ]),


    html.Br(),
    html.Div([
            dcc.Dropdown(listOfHours,
                         placeholder='Select an Hour', id='hour_sections'),
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
    # print("text: " + str(blk_name))
    # print("day: " + str(day_value))
    # print("hour: " + str(hour_value))
    filtered_df = df.copy()

    if day_value is not None and hour_value is not None:
        filtered_df['PAY_AMOUNT'] = getCosts(day_value, hour_value)
    else:
        filtered_df['PAY_AMOUNT'] = df['PAY_AMOUNT']

    if blk_name is None or blk_name.upper() not in street_names:
        # filtered_df = df.copy()
        boston_map = px.scatter_mapbox(
            filtered_df,
            lat=filtered_df['LATITUDE'],
            lon=filtered_df['LONGITUDE'],
            color='PAY_AMOUNT',
            zoom=13,
            custom_data=['STREET', 'LATITUDE', 'LONGITUDE']
        )
        boston_map.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
    else:
        # print(blk_name.upper())
        filtered_df = filtered_df[filtered_df["STREET_NAMES"] == blk_name.upper()]
        # temp additional zoom determined via number of locations
        # can maybe try calculating distance between meters
        if len(filtered_df) < 5:
            boston_map = px.scatter_mapbox(
                filtered_df,
                lat=filtered_df['LATITUDE'],
                lon=filtered_df['LONGITUDE'],
                color='PAY_AMOUNT',
                zoom=16,
                custom_data=['STREET', 'LATITUDE', 'LONGITUDE']
            )
            #boston_map.update_traces(marker=dict(size=10, color="green"))
            boston_map.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
        else:

            boston_map = px.scatter_mapbox(
                filtered_df,
                lat=filtered_df['LATITUDE'],
                lon=filtered_df['LONGITUDE'],
                color='PAY_AMOUNT',
                zoom=15.5,
                custom_data=['STREET', 'LATITUDE', 'LONGITUDE']
            )
            #boston_map.update_traces(marker=dict(size=10, color="green"))
            boston_map.update_traces(marker=dict(size=10), selector=dict(mode='markers'))

    boston_map.update_layout(mapbox_style="open-street-map")
    boston_map.update_layout(height=900, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    boston_map.update_traces(
        hovertemplate="<br>".join([
            "Street: %{customdata[0]}",
            "Latitude: %{customdata[1]}",
            "Longitude: %{customdata[2]}",
            # "Pay Period: %{customdata[3]}",
        ]))
    return boston_map


if __name__ == '__main__':
    app.run_server(debug=True)