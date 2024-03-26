def add_station(driver, name, lat, lng, id):
    driver.execute_query(
        "MERGE (s:Station {name: $name, lat: $lat, lng: $lng, id: $id})",
        name=name, lat=lat, lng=lng, id=id, database_="neo4j",
    )

