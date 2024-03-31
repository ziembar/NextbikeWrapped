def add_station(driver, name, lat, lng):
    driver.execute_query(
        "MERGE (s:Station {name: $name, lat: $lat, lng: $lng})",
        name=name, lat=lat, lng=lng, database_="neo4j",
    )
    



def find_station_by_coordinates(driver, lat, lng):
    lat = round(float(lat), 4)
    lng = round(float(lng), 4)
    query = """
    MATCH (s:Station)-[r]-(d:Station)
    WHERE round(s.lat, 4) = $lat AND round(s.lng, 4) = $lng
    RETURN s, r, d
    """
    result = driver.execute_query(query, lat=lat, lng=lng, database_="neo4j")
    driver.close()
    return result[0]
    


def add_distance_relation(driver, lat1, lng1, lat2, lng2, distance, time):
    lat1 = round(float(lat1), 4)
    lng1 = round(float(lng1), 4)

    lat2 = round(float(lat2), 4)
    lng2 = round(float(lng2), 4)

    query = """
    MATCH (s1:Station)
    WHERE round(s1.lat, 4) = $lat1 AND round(s1.lng, 4) = $lng1
    MATCH (s2:Station)
    WHERE round(s2.lat, 4) = $lat2 AND round(s2.lng, 4) = $lng2
    MERGE (s1)-[r:PATH]->(s2)
    SET r.distance = $distance
    SET r.time = $time
    """
    driver.execute_query(query, lat1=lat1, lng1=lng1, lat2=lat2, lng2=lng2, distance=distance, time=time, database_="neo4j")
    driver.close()

