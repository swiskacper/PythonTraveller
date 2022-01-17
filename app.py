import time

from flask import Flask, request
import requests
import Map
import Util
import city
import weather
import overpy

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'hello!'


@app.route('/')
def search_city():
    c1 = get_City()
    API_KEY = 'd2b60a612ecb829daf83449f9fe86395'
    currentCity = request.args.get('q')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={c1.name}&APPID={API_KEY}'
    response = requests.get(url).json()
    w1 = weather.Weather(c1.name, round(response.get('main', {}).get('temp') - 273.15, 2),
                         response.get('wind', {}).get('speed'),
                         response.get('clouds', {}).get('all'))
    getOverpassResult(c1, w1)
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {c1.name}. Error message = {message}'
    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        return w1.toJSON()
    else:
        return f'Error getting temperature for {currentCity.title()}'


def getOverpassResult(currentCity: city, currentWeather: weather):
    bounds = [float(currentCity.lon) - 0.6, float(currentCity.lat) - 0.6, float(currentCity.lon) + 0.6,
              float(currentCity.lat) + 0.6]
    # sunnyAttracions = ['"leisure"="park"', '"tourism"="museum"']
    kindOfPlace, sunnyAttracions, things = getPlacesToOverpass(currentWeather)
    overpyRequester = overpy.Overpass()
    resultTuple = []
    k = 1
    for element in sunnyAttracions:
        # http://www.overpass-api.de/api/status
        time.sleep(15)
        try:
            resultTuple.append(overpyRequester.query(Util.makeAQuery(bounds, element, things)))
        except Exception as e:
            print(e)
            getOverpassResult(currentCity, currentWeather)
        k = k + 1

    Map.display_map(resultTuple, [currentCity.lat, currentCity.lon], kindOfPlace, currentWeather)


def getPlacesToOverpass(currentWeather: weather) -> tuple:
    if currentWeather.temp < 15:
        sunnyAttracions = ['"amenity"="cinema"', '"tourism"="museum"']
        kindOfPlace = ['cinema', 'museum']
        # kindOfPlace = ['cinema', 'museum', 'park', 'restaurant', 'theatre']
        things = ['node', 'way', 'relation']
    else:
        sunnyAttracions = ['"amenity"="cinema"', '"tourism"="museum"',
                           '"amenity"="restaurant"', '"amenity"="theatre"']
        # kindOfPlace = ['cinema', 'museum']
        kindOfPlace = ['cinema', 'museum', 'restaurant', 'theatre']
        things = ['node', 'way', 'relation']
    return kindOfPlace, sunnyAttracions, things


def get_City() -> city:
    response1 = requests.get('https://ipinfo.io/json').json()
    data = response1.get('loc')
    c1 = city.City(response1.get("city"), data.split(',')[0], data.split(',')[1])
    return c1


if __name__ == '__main__':
    app.run()
