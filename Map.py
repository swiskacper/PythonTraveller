import requests
from numpy import array

import Util
import random
import plotly.graph_objects as go
import copy
import weather
import lista

accesstokenMapbox = 'pk.eyJ1Ijoic3dpc2thY3BlciIsImEiOiJja3k4bWk2ZzgxNGVjMnBub2R5Y2xrZWN4In0.CaeWG-UQNST74lph1zXXgQ'


def display_map(coords, startCoord, kindOfPlace, weather: weather):
    latHeatMap, lonHeatMap = getBorderCoords("driving", "30", startCoord)
    print(len(coords))
    fig = makeAMap(coords, kindOfPlace, latHeatMap, lonHeatMap, startCoord, weather)

    fig.show()


def makeAMap(coords, kindOfPlace, latBorder, lonBorder, startCoord, weather: weather):
    markerTemplate = dict(
        size=9,
        color='#0000FF',
        colorscale='Viridis')

    fig, markerCurrent = createCurrentLocalizaitionMarker(markerTemplate, startCoord)

    borderMarker = copy.deepcopy(markerTemplate)

    createBorder(fig, latBorder, lonBorder, borderMarker)
    latBordersDriving60, lonBordersDriving60 = getBorderCoords("driving", "60", startCoord)
    latBordersDriving30, lonBordersDriving30 = getBorderCoords("driving", "30", startCoord)
    latBordersDriving15, lonBordersDriving15 = getBorderCoords("driving", "15", startCoord)
    latBordersWalking30, lonBordersWalking30 = getBorderCoords("walking", "30", startCoord)
    latBordersWalking60, lonBordersWalking60 = getBorderCoords("walking", "60", startCoord)
    latBordersWalking15, lonBordersWalking15 = getBorderCoords("walking", "15", startCoord)
    latBordersCycling15, lonBordersCycling15 = getBorderCoords("cycling", "15", startCoord)
    latBordersCycling30, lonBordersCycling30 = getBorderCoords("cycling", "30", startCoord)
    latBordersCycling60, lonBordersCycling60 = getBorderCoords("cycling", "60", startCoord)
    idx = 0
    markersPOILON = []
    markersPOI = []
    markersPOILAT = []
    for i in range(len(coords)):
        comments, lat, lon = Util.getLatLonAndComments(coords[i])
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        newMarker = copy.deepcopy(markerTemplate)
        newMarker['color'] = color
        markersPOI.append(newMarker)
        markersPOILON.append(dict(lat))
        markersPOILAT.append(dict(lon))
        createPointOfIntrest(comments, fig, idx, kindOfPlace, lat, lon, newMarker)
        idx = idx + 1

    setMapProperties(fig, startCoord)

    lista1 = lista
    print(len(markersPOI))
    print(len(markersPOILAT))
    print(len(markersPOILON))

    print((markersPOI))
    print((markersPOILAT))
    print((markersPOILON))

    fig.update_layout(
        updatemenus=list([
            dict(buttons=list([
                dict(
                    args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersDriving60, markersPOILAT),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersDriving60, markersPOILON),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Driving 60',
                    method='update',
                    # 'mode':'lines'
                ), dict(
                    args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersDriving30, markersPOILAT),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersDriving30, markersPOILON),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Driving 30',
                    method='update',
                    # 'mode':'lines'
                ), dict(
                    args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersDriving15, markersPOILAT[0]),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersDriving15, markersPOILON[0]),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Driving 15',
                    method='update',
                    # 'mode':'lines'
                ), dict(
                    args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersCycling60, markersPOILAT[0]),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersCycling60, markersPOILON[0]),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Cycling 60',
                    method='update',
                    # 'mode':'lines'
                ), dict(
                    args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersCycling30, markersPOILAT[0]),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersCycling30, markersPOILON[0]),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Cycling 30',
                    method='update',
                    # 'mode':'lines'
                ), dict(
                    args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersCycling15, markersPOILAT[0]),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersCycling15, markersPOILON[0]),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Cycling 15',
                    method='update',
                    # 'mode':'lines'
                ), dict(
                    args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersWalking60, markersPOILAT),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersWalking60, markersPOILON),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Walking 60',
                    method='update',
                    # 'mode':'lines'
                ), createaDict(latBordersWalking30, lista1, lonBordersWalking30, borderMarker, markerCurrent, markersPOI,
                               markersPOILAT, markersPOILON, startCoord, "Walking 30"),
                dict(args=[{'marker': lista1.lat([markerCurrent], [borderMarker], markersPOI),
                           'lon': lista1.lat([float(startCoord[0])], latBordersWalking15, markersPOILAT[0]),
                           'lat': lista1.lat([float(startCoord[1])], lonBordersWalking15, markersPOILON[0]),
                           'mode': ['markers', 'lines', 'markers']}],
                    label='Walking 15',
                    method='update',
                    # 'mode':'lines'
                ),

            ]),
            )
        ])
    )

    fig.update_layout(
        title_x=0.5,
        title_y=0.97,
        title_text=weather.toString(),
    )

    return fig


def createaDict(latBordersWalking30, lista1, lonBordersWalking30, marker1, markerCurrent, markers2, markersLat2,
                markersLon2, startCoord, label):
    return dict(
        args=[{'marker': lista1.lat([markerCurrent], [marker1], markers2),
               'lon': lista1.lat([float(startCoord[0])], latBordersWalking30, markersLat2[0]),
               'lat': lista1.lat([float(startCoord[1])], lonBordersWalking30, markersLon2[0]),
               'mode': ['markers', 'lines', 'markers']}],
        label=label,
        method='update',
        # 'mode':'lines'
    )


def setMapProperties(fig, startCoord):
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


def createPointOfIntrest(comments, fig, idx, kindOfPlace, lat, lon, newMarker):
    fig.add_trace(go.Scattermapbox(
        lat=lat,
        lon=lon,
        mode='markers',
        marker=newMarker,
        text=comments,
        name=kindOfPlace[idx]

    ),
    )


def createBorder(fig, latBorder, lonBorder, marker1):
    fig.add_trace(go.Scattermapbox(
        lat=lonBorder,
        lon=latBorder,
        mode='lines',
        marker=marker1,
        text=" ",
        name="Border"
    ))


def createCurrentLocalizaitionMarker(markerTemplate, startCoord):
    markerCurrent = copy.deepcopy(markerTemplate)
    markerCurrent['color'] = '#008000'
    print()
    fig = go.Figure(go.Scattermapbox(
        lat=array(float((startCoord[1]))),
        lon=array(float((startCoord[0]))),
        mode='markers',
        marker=markerCurrent,
        text="Your localization",
        name="Current location"
    ))
    return fig, markerCurrent


def changeLines(fig, latHeatMap, lonHeatMap):
    fig.add_trace(go.Scattermapbox(
        lat=lonHeatMap,
        lon=latHeatMap,
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=9,
            color='#0000FF',
        ),
        text=" ",
        name="Border"
    ))

    return latHeatMap, lonHeatMap


def getBorderCoords(vehicle, minutes, startCoord):
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
