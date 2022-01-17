import json


def makeAQuery(bounds: list, sunnyAttracions: str, things: list) -> str:
    query = """
           [out:json][timeout:500];
    ("""
    for element in things:
        query = query + element + '[' + sunnyAttracions + ']' + '(' + str(bounds[0]) + ',' + str(
            bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[3]) + ');'

    query = query + ");out body;>;out skel qt;"
    return query


def getLatLonAndComments(coords: tuple) -> tuple:
    lat = []
    lon = []
    comments = []
    for element in coords.ways:
        comment = ''
        lat.append(float(element.nodes[0].lat))
        lon.append(float(element.nodes[0].lon))
        string = json.loads(json.dumps(element.tags))
        str2 = tuple(element.tags)
        for element2 in str2:
            comment = comment + element2 + ":" + string[element2] + "<br>"
        comments.append(comment)
    return comments, lat, lon
