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
    sunnyAttracions = ['"leisure"="park"']
    # sunnyAttracions = ['"amenity"="cinema"', '"tourism"="museum"', '"leisure"="park"', '"amenity"="food_court"']
    kindOfPlace = ['cinema']
    # kindOfPlace = ['cinema', 'museum', 'park', 'food_court']
    things = ['node', 'way', 'relation']
    api = overpy.Overpass()
    resultTuple = []
    k=1
    for i in range(len(sunnyAttracions)):
        time.sleep(i)
        resultTuple.append(api.query(Util.makeAQuery(bounds, sunnyAttracions[i], things)))
        k=k + 1

    print("RESULT TUPLE")
    print(resultTuple[0].ways)
    Map.display_map(resultTuple, [city.lat, city.lon], kindOfPlace)


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
