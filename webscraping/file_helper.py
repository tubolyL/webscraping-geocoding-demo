import json
import time
from os import stat
from os.path import exists
from converter import geocode, geocode_avg

curr_time = time.strftime("%Y%m%d-%H%M%S")


def update_file(details, file):
    for parameter in details:
        file["records"].append(
            {
                'address': parameter[0],
                'price': parameter[1],
                'rooms': parameter[2],
                'area_size': parameter[3]
            }
        )
    return file


def initialize_json(filename):

    if not exists('files/' + filename + curr_time + ".json"):
        with open('files/' + filename + curr_time + ".json", "w") as file:
            json.dump({"records": []}, file)
    if stat('files/' + filename + curr_time + ".json").st_size == 0:
        with open('files/' + filename + ".json", "w+") as file:
            json.dump({"records": []}, file)


def write_details(details, filename):
    with open('files/' + filename + curr_time + ".json", "r+") as file:
        data = json.load(file)
        data = update_file(details, data)
        file.seek(0)
        json.dump(data, file)
    geocoded = geocode.geocode('files/' + filename + curr_time)
    geocoded_avg = geocode_avg.geocode('files/' + filename + curr_time)
    with open('../converter/converted-files/'+filename+curr_time+'_all.json', 'w') as output:
        json.dump(geocoded, output)
    with open('../converter/converted-files/'+filename+curr_time+'_avg.json', 'w') as output:
        json.dump(geocoded_avg, output)
