def add_station(driver, name, lat, lng, uid, city_id):
    driver.execute_query(
        "MERGE (s:Station {name: $name, lat: $lat, lng: $lng, uid: $uid, city_id: $city_id})",
        name=name, lat=lat, lng=lng, database_="neo4j",
    )
    



def find_station_by_coordinates(driver, lat, lng):
    lat = float(lat)
    lng = float(lng)
    query = """
    MATCH (s:Station)-[r]-(d:Station)
    WHERE round(s.lat, 4) = round($lat, 4) AND round(s.lng, 4) = round($lng, 4)
    RETURN s, r, d
    """
    result = driver.execute_query(query, lat=lat, lng=lng, database_="neo4j")
    driver.close()
    return result[0]



def find_station_by_uid(driver, uid):
    query = """
    MATCH (s:Station)-[r]-(d:Station)
    WHERE s.uid = $uid
    RETURN s, r, d
    """
    result = driver.execute_query(query, uid=uid, database_="neo4j")
    driver.close()
    return result[0]
    


def add_distance_relation(driver, uid1, uid2, distance, time):

    query = """
    MATCH (s1:Station)
    WHERE s1.uid = $uid1
    MATCH (s2:Station)
    WHERE s2.uid = $uid2
    MERGE (s1)-[r:PATH]->(s2)
    SET r.distance = $distance
    SET r.time = $time
    """
    driver.execute_query(query, uid1=uid1, uid2=uid2, distance=distance, time=time, database_="neo4j")
    driver.close()

