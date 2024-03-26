def add_station(driver, name, lat, lng, id):
    driver.execute_query(
        "MERGE (s:Station {name: $name, lat: $lat, lng: $lng, id: $id})",
        name=name, lat=lat, lng=lng, database_="neo4j",
    )



def find_station_by_coordinates(driver, lat, lng):
    query = """
    MATCH (s:Station)
    WHERE round(s.lat, 4) = round($lat, 4) AND round(s.lng, 4) = round($lng, 4)
    RETURN s
    """
    result = driver.execute_query(query, lat=lat, lng=lng, database_="neo4j")
    return result