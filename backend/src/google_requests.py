import googlemaps
from decouple import config
from Models import getDriver
import db_actions
import math
import requests
import base64


def distance_matrix_request(rentals):
    origin = {"lat": rentals[0]['startPlace']['lat'], "lng": rentals[0]['startPlace']['lng']}
    destinations = []
    for rent in rentals:
        destinations.append({"lat": rent['endPlace']['lat'], "lng": rent['endPlace']['lng']})

    
    gmaps = googlemaps.Client(key=config('GOOGLE_API_KEY'))
    result = gmaps.distance_matrix(origin, destinations, mode='bicycling')

    print("1 request, destinations - ", len(destinations))
    total_distance = 0

    for dest, res in zip(rentals, result['rows'][0]['elements']):
        amount = dest.get('amount', 1)
        if 'amount' in dest:
            db_actions.add_distance_relation(getDriver(), origin['lat'], origin['lng'], dest['endPlace']['lat'], \
                                dest['endPlace']['lng'], res['distance']['value'], res['duration']['value'])
        total_distance += res['distance']['value'] * amount
    return total_distance







def static_map_request(g_rentals):
    min_lat, min_lng, max_lat, max_lng = __find_bounds(g_rentals)
    center_lat = (min_lat + max_lat)/2
    center_lng = (min_lng + max_lng)/2

    zoom = __getZoom(min_lat, min_lng, max_lat, max_lng)

    url = f'https://maps.googleapis.com/maps/api/staticmap?center={center_lat},{center_lng}&zoom={zoom}&scale=2&size=640x640&maptype=roadmap&key={config("GOOGLE_API_KEY")}&style=feature:all|element:labels.icon|visibility:off&'
    

    paths = []
    for route in g_rentals:
        place = f"{route['startPlace']['lat']},{route['startPlace']['lng']}|{route['endPlace']['lat']},{route['endPlace']['lng']}"
        times_traveled = route['amount']

        # Create path style
        path_style = f'path=color:0x966A91A9|weight:{math.ceil(math.sqrt(times_traveled))*2}|geodesic:true'

        # Create path locations

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

    return math.ceil(max(lngZoom, latZoom))


def __find_bounds(rentals):
    min_lat = float('inf')
    max_lat = float('-inf')
    min_lng = float('inf')
    max_lng = float('-inf')
    
    for rent in rentals:
        start_lat = rent['startPlace']['lat']
        start_lng = rent['startPlace']['lng']
        end_lat = rent['endPlace']['lat']
        end_lng = rent['endPlace']['lng']
        
        min_lat = min(min_lat, start_lat, end_lat)
        max_lat = max(max_lat, start_lat, end_lat)
        min_lng = min(min_lng, start_lng, end_lng)
        max_lng = max(max_lng, start_lng, end_lng)
    
    return min_lat, min_lng, max_lat, max_lng