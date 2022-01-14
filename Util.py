import json


def makeAQuery(bounds, sunnyAttracions, things):
    query = """
           [out:json][timeout:500];
    ("""
    for k in range(len(things)):
            query = query + things[k] + '[' + sunnyAttracions + ']' + '(' + str(bounds[0]) + ',' + str(
                bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[3]) + ');'

    query = query + ");out body;>;out skel qt;"
    return query



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
            comment = comment + str2[k] + ":" + str[str2[k]] + "<br>"
        comments.append(comment)
    return comments, lat, lon

