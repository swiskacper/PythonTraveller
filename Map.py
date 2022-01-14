import requests

import Util
import random
import plotly.graph_objects as go

accesstokenMapbox = 'pk.eyJ1Ijoic3dpc2thY3BlciIsImEiOiJja3k4bWk2ZzgxNGVjMnBub2R5Y2xrZWN4In0.CaeWG-UQNST74lph1zXXgQ'


def display_map(coords, startCoord, kindOfPlace):
    latHeatMap, lonHeatMap = getHeatCoords("driving", "30", startCoord)
    latHeatMap1, lonHeatMap1 = getHeatCoords("driving", "60", startCoord)
    latHeatMap2, lonHeatMap2 = getHeatCoords("walking", "30", startCoord)
    latHeatMap3, lonHeatMap3 = getHeatCoords("walking", "60", startCoord)

    fig = makeAMap(coords, kindOfPlace, latHeatMap, lonHeatMap, startCoord)

    print("SSSSSS")
    print("SSSSSS")
    print("SSSSSS")
    print(len(latHeatMap))
    print("QQQQQ")
    print(latHeatMap)
    print(latHeatMap)
    print(latHeatMap)
    for i in range(len(latHeatMap)):
        if i>=len(latHeatMap3) or i>=len(latHeatMap2):
            break
        fig.update_layout(
            updatemenus=list([
                dict(buttons=list([
                    dict(
                        args=[{'marker': [latHeatMap[i]], 'lat': [latHeatMap3[i]], 'lon': [lonHeatMap3[i]]}],
                        label='var1',
                        method='update'
                    ),
                    dict(
                        args=[{'marker': [latHeatMap[i]], 'lat': [latHeatMap2[i]], 'lon': [lonHeatMap2[i]]}],
                        label='var1',
                        method='update'
                    ),
                    dict(label="Cluster 1",
                         method="update",
                         args=["shapes", makeAMap(coords, kindOfPlace, latHeatMap2, lonHeatMap2, startCoord)]),

                ]),
                )
            ])
        )

    fig.update_layout(
        title_text="Traveller",
    )


    fig.show()
    return "SSS"


def makeAMap(coords, kindOfPlace, latHeatMap, lonHeatMap, startCoord):
    lat = []
    lon = []
    lat.append(float(startCoord[0]))
    lon.append(float(startCoord[1]))

    fig = go.Figure(go.Scattermapbox(
        lat=lon,
        lon=lat,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14,
            color='#008000',

        ),
        text="Your localization",
        name="Current location"
    ))

    changeLines(fig, latHeatMap, lonHeatMap)

    idx = 0

    for i in range(len(coords)):
        comments, lat, lon = Util.getLatLonAndComments(coords[i])
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        print(comments)
        fig.add_trace(go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14,
                color=color,

            ),
            text=comments,
            name=kindOfPlace[idx]

        ),
        )
        if idx < len(kindOfPlace):
            idx = idx + 1

    lat = []
    lon = []
    lat.append(float(startCoord[0]))
    lon.append(float(startCoord[1]))

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=accesstokenMapbox,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=lon[0],
                lon=lat[0]
            ),
            pitch=0,
            zoom=5

        )
    )
    return fig


def changeLines(fig, latHeatMap, lonHeatMap):
    fig.add_trace(go.Scattermapbox(
        lat=lonHeatMap,
        lon=latHeatMap,
        mode='lines',
        marker=go.scattermapbox.Marker(
            size=14,
            color='#0000FF',

        ),
        text=" ",
        name="Border"
    ))

    return latHeatMap,lonHeatMap


def getHeatCoords(vehicle, minutes, startCoord):
    prefix = "https://api.mapbox.com/isochrone/v1/mapbox/"
    postfix = "&polygons=true&access_token="
    uri = prefix + vehicle + '/' + startCoord[0] + ',' + startCoord[
        1] + '?' + 'contours_minutes=' + minutes + postfix + accesstokenMapbox
    result = requests.get(uri).json()
    print(result['features'][0]['geometry']['coordinates'][0])
    print(len(result['features'][0]['geometry']['coordinates'][0]))
    result2 = result['features'][0]['geometry']['coordinates'][0]
    lat = []
    lon = []
    for i in range(len(result2)):
        lat.append(result2[i][0])
        lon.append(result2[i][1])
    return lat, lon
