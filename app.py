import time

from flask import Flask, request
import requests, json

import Map
import Util
import city
import weather
import geocoder
import overpy

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'dddd!'


@app.route('/city')
def search_city():
    c1 = get_City()
    API_KEY = 'd2b60a612ecb829daf83449f9fe86395'
    city = request.args.get('q')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={c1.name}&APPID={API_KEY}'
    response = requests.get(url).json()
    w1 = weather.Weather(c1.name, round(response.get('main', {}).get('temp') - 273.15, 2),
                         response.get('wind', {}).get('speed'),
                         response.get('clouds', {}).get('all'))
    getApiResult(c1, w1)
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {c1.name}. Error message = {message}'
    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        return w1.toJSON()
    else:
        return f'Error getting temperature for {city.title()}'


def getApiResult(city, weather):
    bounds = [float(city.lon) - 0.1, float(city.lat) - 0.1, float(city.lon) + 0.1, float(city.lat) + 0.1]
    print(bounds)
    sunnyAttracions = ['"leisure"="park"', '"tourism"="museum"']
    # sunnyAttracions = ['"amenity"="cinema"', '"tourism"="museum"', '"leisure"="park"', '"amenity"="food_court"']
    kindOfPlace = ['cinema', 'museum']
    # kindOfPlace = ['cinema', 'museum', 'park', 'food_court']
    things = ['node', 'way', 'relation']
    api = overpy.Overpass()
    resultTuple = []
    k = 1
    for i in range(len(sunnyAttracions)):
        # http://www.overpass-api.de/api/status
        time.sleep(5)
        resultTuple.append(api.query(Util.makeAQuery(bounds, sunnyAttracions[i], things)))
        k = k + 1

    Map.display_map(resultTuple, [city.lat, city.lon], kindOfPlace, weather)


def get_City() -> city:
    g = geocoder.ip('me')
    response1 = requests.get('http://ipinfo.io/json').json()
    data = response1.get('loc')
    c1 = city.City(response1.get("city"), data.split(',')[0], data.split(',')[1])
    return c1


if __name__ == '__main__':
    app.run()
