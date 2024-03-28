import requests
import defs
from decouple import config
from neo4j import GraphDatabase
from Models import Station, getDriver

#! WARNING: This script can overwrite the database 

stations = defs.get_all_stations()

stationNodes = []
for station in stations:
    if station['bike'] == False:
        stationNodes.append({"name": station['name'], "number": station['number'], "lat": station['lat'], "lng": station['lng']})

Station.create_or_update(*stationNodes)
getDriver().close()