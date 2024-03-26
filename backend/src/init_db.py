import requests
from dotenv import load_dotenv
from decouple import config
from neo4j import GraphDatabase
import db_actions
load_dotenv()


response = requests.get("https://api.nextbike.net/maps/nextbike-live.json?city=812")
stations = response.json()['countries'][0]['cities'][0]['places']


uri = config('NEO4J_URI')
auth = (config('NEO4J_USERNAME'), config('NEO4J_PASSWORD'))

driver = GraphDatabase.driver(uri, auth=auth)

# for station in stations:
    # if station['bike'] == False:
        # print(station['name'], station['lat'], station['lng'])




# db_actions.add_station(driver, "test", 1, 2, "420")
print(db_actions.find_station_by_coordinates(driver, 1, 2))


driver.close()  # close the driver object

