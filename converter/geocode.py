from unidecode import unidecode
import pandas as pd
import json


def geocode(filename):
    data = pd.read_json(filename+'.json')
    coordinates = open('../converter/coordinates.json')

    file = json.load(coordinates)
    feature = {}
    geodata = {'type': 'FeatureCollection', 'features': []}

    for d in data['records']:
        for f in file['records']:
            if (f['name'] in unidecode(d['address']).lower().replace(',', '').replace('-', '').split() and 'kerulet'
                    not in unidecode(d['address']).lower().replace(',', '').replace('-', '').split()):
                feature = {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(f['coordinates']['east']),
                            float(f['coordinates']['north'])
                        ]
                    },
                    "type": "Feature",
                    "properties": {
                        "address": d['address'],
                        "price": d['price'],
                        "rooms": d['rooms'],
                        "area_size": d['area_size'],
                    }
                }
                geodata['features'].append(feature)
    for d in data['records']:
        if 'kerulet' in unidecode(d['address']).lower():
            feature = {
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float('19.041726'),
                        float('47.484694')
                    ]
                },
                "type": "Feature",
                "properties": {
                    "address": d['address'],
                    "price": d['price'],
                    "rooms": d['rooms'],
                    "area_size": d['area_size'],
                }
            }
            geodata['features'].append(feature)
    return geodata
