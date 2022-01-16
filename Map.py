import requests
from numpy import array
from plotly.graph_objs import Figure, Marker

import Util
import random
import plotly.graph_objects as go
import copy
import weather

accesstokenMapbox = 'pk.eyJ1Ijoic3dpc2thY3BlciIsImEiOiJja3k4bWk2ZzgxNGVjMnBub2R5Y2xrZWN4In0.CaeWG-UQNST74lph1zXXgQ'


def display_map(coords: list, startCoord: list, kindOfPlace: list, currentWeather: weather):
    latBorder, lonBorder = getBorderCoords("driving", "60", startCoord)
    fig = makeAMap(coords, kindOfPlace, latBorder, lonBorder, startCoord, currentWeather)
    fig.show()


def makeAMap(coords: list, kindOfPlace: list, latBorder: list, lonBorder: list, startCoord: list,
             currentWeather: weather) -> Figure:
    markerTemplate = dict(
        size=12,
        colorscale='Viridis')

    fig, markerCurrent = createCurrentLocalizaitionMarker(markerTemplate, startCoord)
    borderMarker = copy.deepcopy(markerTemplate)
    createBorder(fig, latBorder, lonBorder, borderMarker)
    idx = 0
    markersPOILON = []
    markersPOI = []
    markersPOILAT = []
    for i in range(len(coords)):
        createPOIs(coords, fig, i, idx, kindOfPlace, markerTemplate, markersPOI, markersPOILAT, markersPOILON)
        idx = idx + 1
    setMapProperties(fig, startCoord)
    makeDropDownList(borderMarker, fig, markerCurrent, markersPOI, markersPOILAT, markersPOILON, startCoord)
    makeText(fig, currentWeather)

    return fig


def makeText(fig: Figure, currentWeather: weather):
    fig.update_layout(
        title_x=0.5,
        title_y=0.97,
        title_text=currentWeather.toString(),
    )


def createPOIs(coords: list, fig: Figure, i: int, idx: int, kindOfPlace: list, markerTemplate: dict,
               markersPOI: list, markersPOILAT: list, markersPOILON: list):
    comments, lat, lon = Util.getLatLonAndComments(coords[i])
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    newMarker = copy.deepcopy(markerTemplate)
    newMarker['color'] = color
    markersPOI.append(newMarker)
    markersPOILON.append(lat)
    markersPOILAT.append(lon)
    createPointOfIntrest(comments, fig, idx, kindOfPlace, lat, lon, newMarker)


def makeDropDownList(borderMarker: dict, fig: Figure, markerCurrent: dict, markersPOI: list, markersPOILAT: list,
                     markersPOILON: list, startCoord: list):
    fig.update_layout(
        updatemenus=list([
            dict(buttons=list([
                makeADict(borderMarker, getBorderCoords("driving", "60", startCoord), markerCurrent, markersPOI,
                          markersPOILAT, markersPOILON, startCoord, "Driving 60"),
                dict(
                    makeADict(borderMarker, getBorderCoords("driving", "30", startCoord), markerCurrent, markersPOI,
                              markersPOILAT, markersPOILON, startCoord, "Driving 30"),
                ), dict(
                    makeADict(borderMarker, getBorderCoords("driving", "15", startCoord), markerCurrent, markersPOI,
                              markersPOILAT, markersPOILON, startCoord, "Driving 15"),
                ), dict(
                    makeADict(borderMarker, getBorderCoords("cycling", "60", startCoord), markerCurrent, markersPOI,
                              markersPOILAT, markersPOILON, startCoord, "Cycling 60"),
                ), dict(
                    makeADict(borderMarker, getBorderCoords("cycling", "30", startCoord), markerCurrent, markersPOI,
                              markersPOILAT, markersPOILON, startCoord, "Cycling 30"),
                ), dict(
                    makeADict(borderMarker, getBorderCoords("cycling", "15", startCoord), markerCurrent, markersPOI,
                              markersPOILAT, markersPOILON, startCoord, "Cycling 15"),
                ), dict(
                    makeADict(borderMarker, getBorderCoords("walking", "60", startCoord), markerCurrent, markersPOI,
                              markersPOILAT, markersPOILON, startCoord, "Walking 60"),
                ),
                dict(makeADict(borderMarker, getBorderCoords("walking", "30", startCoord), markerCurrent, markersPOI,
                               markersPOILAT, markersPOILON, startCoord, "Walking 30"),
                     ),
                dict(makeADict(borderMarker, getBorderCoords("walking", "15", startCoord), markerCurrent, markersPOI,
                               markersPOILAT, markersPOILON, startCoord, "Walking 15"),
                     ),

            ]),
            )
        ])
    )


def makeADict(borderMarker: dict, latBorders: tuple, markerCurrent: dict, markersPOI: list, markersPOILAT: list,
              markersPOILON: list, startCoord: list, label: str) -> dict:
    return dict(
        args=[{'marker': makeResult([markerCurrent], [borderMarker], markersPOI),
               'lon': makeResult([float(startCoord[0])], latBorders[0], markersPOILAT),
               'lat': makeResult([float(startCoord[1])], latBorders[1], markersPOILON),
               'mode': ['markers', 'lines', 'markers','markers','markers','markers']}],
        label=label,
        method='update',
    )


def setMapProperties(fig: Figure, startCoord: list):
    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=accesstokenMapbox,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=(float((startCoord[1]))),
                lon=(float((startCoord[0])))
            ),
            pitch=0,
            zoom=10

        )
    )


def createPointOfIntrest(comments: str, fig: Figure, idx: int, kindOfPlace: list, lat: float, lon: float,
                         newMarker: dict):
    fig.add_trace(go.Scattermapbox(
        lat=lat,
        lon=lon,
        mode='markers',
        marker=newMarker,
        text=comments,
        name=kindOfPlace[idx]
    ), )


def createBorder(fig: Figure, latBorder: list, lonBorder: list, marker1: dict):
    fig.add_trace(go.Scattermapbox(
        lat=lonBorder,
        lon=latBorder,
        mode='lines',
        marker=marker1,
        text=" ",
        name="Border"))


def createCurrentLocalizaitionMarker(markerTemplate: dict, startCoord: list) -> (Figure, Marker):
    markerCurrent = copy.deepcopy(markerTemplate)
    markerCurrent['color'] = '#008000'
    markerCurrent['size'] = 12
    fig = go.Figure(go.Scattermapbox(
        lat=array(float((startCoord[1]))),
        lon=array(float((startCoord[0]))),
        mode='markers',
        marker=markerCurrent,
        text="Your localization",
        name="Current location"))
    return fig, markerCurrent


def changeLines(fig: Figure, latBorder: list, lonBorder: list) -> (list, list):
    fig.add_trace(go.Scattermapbox(
        lat=lonBorder,
        lon=latBorder,
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=12),
        text=" ",
        name="Border"))
    return latBorder, lonBorder


def getBorderCoords(vehicle: str, minutes: str, startCoord: list) -> (list, list):
    prefix = "https://api.mapbox.com/isochrone/v1/mapbox/"
    postfix = "&polygons=true&access_token="
    uri = prefix + vehicle + '/' + startCoord[0] + ',' + startCoord[
        1] + '?' + 'contours_minutes=' + minutes + postfix + accesstokenMapbox
    result = requests.get(uri).json()
    result2 = result['features'][0]['geometry']['coordinates'][0]
    lat = []
    lon = []
    for i in range(len(result2)):
        lat.append(result2[i][0])
        lon.append(result2[i][1])
    return lat, lon


def makeResult(currentLocalizationArg: list, borderArg: list, poiArg: list) -> list:
    result = [currentLocalizationArg, borderArg]
    for i in range(len(poiArg)):
        result.append(poiArg[i])
    return result
