import defs
from Models import Station, getDriver

#! WARNING: This script will overwrite the database 

res = defs.get_all_stations()


stationNodes = []
for country in res['countries']:
    for city in country['cities']:
        for station in city['places']:
            if station['bike'] == False:
                stationNodes.append({"name": station['name'], "uid": station['uid'], "city_id": city['uid'], "lat": station['lat'], "lng": station['lng']})


Station.create_or_update(*stationNodes)
getDriver().close()