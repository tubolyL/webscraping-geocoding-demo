from unidecode import unidecode
import pandas as pd
import json


def geocode(filename):
	data = pd.read_json(filename+'.json')
	coordinates = open('../converter/coordinates.json')

	file = json.load(coordinates)
	feature = {}

	geodata = {'type': 'FeatureCollection', 'features': []}

	for f in file['records']:
		price = 0
		area = 0
		i = 0
		for d in data['records']:
			if (f['name'] in unidecode(d['address']).lower().replace(',', '').replace('-', '').split() and 'kerulet'
					not in unidecode(d['address']).lower().replace(',', '').replace('-', '').split()):
				price += int(d['price'])
				area += int(d['area_size'])
				i += 1

		if i != 0:
			avg_price = float(price) / float(i)
			avg_area = float(area) / float(i)
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
					"price": avg_price,
					"area_size": avg_area,
				}
			}
			geodata['features'].append(feature)

	price = 0
	area = 0
	i = 0
	for d in data['records']:
		if 'kerulet' in unidecode(d['address']).lower():
			price += int(d['price'])
			area += int(d['area_size'])
			i += 1

	if i != 0:
		avg_price = float(price) / float(i)
		avg_area = float(area) / float(i)
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
				"price": avg_price,
				"area_size": avg_area,
			}
		}
		geodata['features'].append(feature)

	return geodata
