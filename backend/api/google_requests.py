import googlemaps
from decouple import config
from Models import getDriver
from db_actions import *
import math
import requests
import base64


def distance_matrix_request(rentals, longest_ride, fastest_ride):
    origin_full = rentals[0]
    origin = {"lat": rentals[0]['start_place_lat'], "lng": rentals[0]['start_place_lng']}
    destinations = []
    for rent in rentals:
        destinations.append({"lat": rent['end_place_lat'], "lng": rent['end_place_lng']})

    

    gmaps = googlemaps.Client(key=config('GOOGLE_API_KEY'))
    result = gmaps.distance_matrix(origin, destinations, mode='bicycling')


    print("1 request, destinations - ", len(destinations))
    total_distance = 0

    for dest, res in zip(rentals, result['rows'][0]['elements']):
        try:
            amount = dest.get('amount')
            if dest['start_place_type'] == 0 and dest['end_place_type'] == 0:
                add_distance_relation(getDriver(), origin_full['start_place'], dest['end_place'],\
                    res['distance']['value'], res['duration']['value'])

            total_distance += res['distance']['value'] * amount

            if longest_ride['distance'] < res['distance']['value']:
                longest_ride['distance'] = res['distance']['value']
                longest_ride['rent'] = dest

            if fastest_ride['velocity'] < (res['distance']['value'] /1000 ) / ((dest['end_time'] - dest['start_time'])/3600):
                fastest_ride['velocity'] = (res['distance']['value'] /1000 ) / ((dest['end_time'] - dest['start_time'])/3600)
                longest_ride['rent'] = dest
        except:
            continue
    return total_distance







def static_map_request(g_rentals):
    min_lat, min_lng, max_lat, max_lng = __find_bounds(g_rentals)
    center_lat = (min_lat + max_lat)/2
    center_lng = (min_lng + max_lng)/2

    zoom = __getZoom(min_lat, min_lng, max_lat, max_lng)

    url = f'https://maps.googleapis.com/maps/api/staticmap?center={center_lat},{center_lng}&zoom={zoom}&scale=2&size=640x640&maptype=roadmap&key={config("GOOGLE_API_KEY")}&style=feature:all|element:labels.icon|visibility:off&'
    

    paths = []
    for route in g_rentals:
        place = f"{route['start_place_lat']},{route['start_place_lng']}|{route['end_place_lat']},{route['end_place_lng']}"
        
        
        times_traveled = route['amount']

        if times_traveled == 1:
            color = '0x808080'  # Gray
        elif 2 <= times_traveled <= 3:
            color = '0xffb84d'  # Yellow
        elif 3 <= times_traveled <= 6:
            color = '0x00FF00'  # Light green
        elif 6 <= times_traveled <= 10:
            color = '0x006400'  # Light green
        else:
            color = '0x006600'  # Dark green

        path_style = f'path=color:{color}|weight:2|geodesic:true'


        # Combine path style and locations
        path = f'{path_style}|{place}'

        paths.append(path)
    paths_str = '&'.join(paths)
    url = url + paths_str
        
    response = requests.get(url)
    if response.status_code == 200:
        encoded_image = base64.b64encode(response.content).decode('utf-8')
        return f'data:image/png;base64, {encoded_image}'
    else:
        return None






def __latRad(lat):
    sin = math.sin(lat * math.pi / 180)
    radX2 = math.log((1 + sin) / (1 - sin)) / 2
    return max(min(radX2, math.pi), -math.pi) / 2

def __getZoom(lat_a, lng_a, lat_b, lng_b):
    latDif = abs(__latRad(lat_a) - __latRad(lat_b))
    lngDif = abs(lng_a - lng_b)

    latFrac = latDif / math.pi
    lngFrac = lngDif / 360

    lngZoom = math.log(1/latFrac) / math.log(2)
    latZoom = math.log(1/lngFrac) / math.log(2)

    return math.ceil(min(lngZoom, latZoom))


def __find_bounds(rentals):
    min_lat = float('inf')
    max_lat = float('-inf')
    min_lng = float('inf')
    max_lng = float('-inf')
    
    for rent in rentals:
        start_lat = rent['start_place_lat']
        start_lng = rent['start_place_lng']
        end_lat = rent['end_place_lat']
        end_lng = rent['end_place_lng']
        
        min_lat = min(min_lat, start_lat, end_lat)
        max_lat = max(max_lat, start_lat, end_lat)
        min_lng = min(min_lng, start_lng, end_lng)
        max_lng = max(max_lng, start_lng, end_lng)
    
    return min_lat, min_lng, max_lat, max_lng