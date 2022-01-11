from flask import Flask, request
import requests, json
from pandas import array
from shapely.speedups._speedups import numpy

import city
import weather
import geocoder
import overpass
import overpy
import array as arr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

app = Flask(__name__)

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")


def display_map(coords):
    comments, lat, lon = getLatLonAndComments(coords)

    fig = go.Figure(go.Scattermapbox(
        lat=lat,
        lon=lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14,
            color='#8B0000'
        ),
        text=comments,
    ))

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1Ijoic3dpc2thY3BlciIsImEiOiJja3k4bWk2ZzgxNGVjMnBub2R5Y2xrZWN4In0.CaeWG-UQNST74lph1zXXgQ',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=lat[0],
                lon=lon[0]
            ),
            pitch=0,
            zoom=5
        )
    )

    fig.show()
    return "SSS"


def getLatLonAndComments(coords):
    lat = []
    lon = []
    comments = []
    for i in range(len(coords.ways)):
        comment = ''
        lat.append(coords.ways[i].nodes[0].lat)
        lon.append(coords.ways[i].nodes[0].lon)
        str = json.loads(json.dumps(coords.ways[i].tags))
        str2 = tuple(coords.ways[i].tags)
        for k in range(len(str2)):
            comment = comment + str2[k] + ":" + str[str2[k]] + "\n"
        comments.append(comment)
    return comments, lat, lon


@app.route('/')
def hello_world():  # put application's code here
    return 'dddd!'


@app.route('/city')
def search_city():
    c1 = get_City()
    API_KEY = 'd2b60a612ecb829daf83449f9fe86395'  # initialize your key here
    city = request.args.get('q')  # city name passed as argument

    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={c1.name}&APPID={API_KEY}'
    response = requests.get(url).json()

    getApiResult(c1)
    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {c1.name}. Error message = {message}'

    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')
    current_wind = response.get('main', {}).get('clouds')
    w1 = weather.Weather(c1.name, round(response.get('main', {}).get('temp') - 273.15, 2),
                         response.get('wind', {}).get('speed'),
                         response.get('clouds', {}).get('all'))

    if current_temperature:
        current_temperature_celsius = round(current_temperature - 273.15, 2)
        return w1.toJSON()
    else:
        return f'Error getting temperature for {city.title()}'


def getApiResult(city):
    bounds = [float(city.lon) - 0.1, float(city.lat) - 0.1, float(city.lon) + 0.1, float(city.lat) + 0.1]
    print(bounds)
    sunnyAttracions = ['"amenity"="cinema"', '"tourism"="museum"', '"leisure"="park"', '"amenity"="food_court"']
    things = ['node', 'way', 'relation']
    api = overpy.Overpass()
    result = api.query(makeAQuery(bounds, sunnyAttracions, things))
    # print("WAYS:")
    # for i in range(len(result.ways)):
    #     print(result.ways[i].nodes[0].lat)
    #     print(result.ways[i].nodes[0].lon)

    # print(result.nodes[0])
    # print(result.relations)
    # print(result.nodes[0].tags)
    display_map(result)


def makeAQuery(bounds, sunnyAttracions, things):
    query = """
           [out:json][timeout:25];
    ("""
    for i in range(len(sunnyAttracions)):
        for k in range(len(things)):
            query = query + things[k] + '[' + sunnyAttracions[i] + ']' + '(' + str(bounds[0]) + ',' + str(
                bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[3]) + ');'
    query = query + ");out body;>;out skel qt;"
    return query


def get_City():
    g = geocoder.ip('me')
    print(g.latlng)
    print(g.city)
    response1 = requests.get('http://ipinfo.io/json').json()
    data = response1.get('loc')
    c1 = city.City(response1.get("city"), data.split(',')[0], data.split(',')[1])
    return c1


if __name__ == '__main__':
    app.run()
