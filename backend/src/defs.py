import time
from decouple import config
import db_actions
import datetime
from Models import getDriver
import requests
import json
import googlemaps



def get_cookie(phone, pin):
        url = "https://account.nextbike.pl/api/login"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://account.nextbike.pl",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": "https://account.nextbike.pl/pl-PL/vw",
            "Accept-Language": "en-US,en;q=0.9",
        }
        data = {
            "mobile": phone,
            "pin": pin,
            "city": "vw",
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        name = response.json().get("screen_name").split()[0].capitalize()

        return response.headers['set-cookie'], name


def get_events(cookie):
    url = "https://account.nextbike.pl/api/events"
    cookies = {
        "Cookie": cookie,
    }
    response = requests.get(url, headers=cookies, cookies=cookies)

    return response.json()


def filter_by_season(data, start, end):
    filtered_data = []
    for rental in data['rentals']:
        if rental['startPlace']['name'] == rental['endPlace']['name']:
            continue
        start_time = rental['startTime']
        end_time = rental['endTime']
        if start_time >= start and end_time <= end:
            filtered_data.append(rental)
    return filtered_data


def filter_last_week(data):
    filtered_data = []
    for rental in data['rentals']:
        start_time = rental['startTime']
        if start_time >= time.time() - 60*60*24*7:
            filtered_data.append(rental)
    return filtered_data

def get_all_stations(): #TODO expand project to include other cities
    response = requests.get("https://api.nextbike.net/maps/nextbike-live.json?city=812")
    return response.json()['countries'][0]['cities'][0]['places']


def top_frequent_rides(data):
    rides = {}
    for rental in data:
        if rental['startPlace']['name'] and rental['endPlace']['name']:
            start_name = rental['startPlace']['name']
            end_name = rental['endPlace']['name']
            ride = f"{min(start_name, end_name)} <---> {max(start_name, end_name)}"
            if ride in rides:
                rides[ride] += 1
            else:
                rides[ride] = 1
    sorted_rides = sorted(rides.items(), key=lambda x: x[1], reverse=True)
    top_rides = sorted_rides[:3]
    return top_rides


def total_time_money_co2_calories(data):
    total_time = 0
    total_cost = 0
    total_co2 = 0
    total_calories = 0

    for rental in data:
        duration = rental['endTime'] - rental['startTime']
        total_time += duration

        total_cost += rental['price']

        total_co2 += rental['co2']

        total_calories += rental['calories']

    return round(total_time/60,1), total_cost/100, total_co2, total_calories





def filter_by_station(data, station):
    filtered_data = []
    for rental in data:
        start_station = rental['startPlace']['name']
        end_station = rental['endPlace']['name']
        if (start_station == station or end_station == station) and (not start_station == None and not end_station == None):
            if end_station == station:
                start_station = rental['endPlace']
                rental['endPlace'] = rental['startPlace']
                rental['startPlace'] = start_station
            filtered_data.append(rental)
    return filtered_data




def group_rentals(data):
    grouped_rentals = []
    for rental in data:
        start_station = rental['startPlace']['name']
        end_station = rental['endPlace']['name']
        found = False
        for existing_rental in grouped_rentals:
            if (existing_rental['startPlace']['name'] == start_station and existing_rental['endPlace']['name'] == end_station):
                existing_rental['amount'] += 1
                found = True
                break
        if not found:
            rental['amount'] = 1
            grouped_rentals.append(rental)
    return grouped_rentals




def total_distance(data):
    total_distance = 0
    stations = {}
    for rental in data:
        start_station = rental['startPlace']['name']
        end_station = rental['endPlace']['name']

        if(start_station == None or end_station == None):
            continue
        if start_station in stations:
            stations[start_station] += 1
        else:
            stations[start_station] = 1
        if end_station in stations:
            stations[end_station] += 1
        else:
            stations[end_station] = 1
    sorted_stations = sorted(stations.items(), key=lambda x: x[1], reverse=True)

    for station in sorted_stations:
        # print("--------STATION: ", station, "-------")
        if len(data) == 0:
            break
        filtered_data = filter_by_station(data, station[0])
        if(len(filtered_data) == 0):
            continue
        grouped_rentals =  group_rentals(filtered_data)

        db_result = db_actions.find_station_by_coordinates(getDriver(), grouped_rentals[0]['startPlace']['lat'], grouped_rentals[0]['startPlace']['lng'])

        for grouped_rent in grouped_rentals.copy():
            for record in db_result:

                # print("pulled from db: ", record['s'].get('name'),"<--->" , record['d'].get('name'))
                # print("comparing ['d'] with: ", grouped_rent['endPlace']['name'])
                if record['d'].get('name') == grouped_rent['endPlace']['name']:
                    # print("its a match!")
                    total_distance += record['r'].get('distance') * grouped_rent['amount']
                    grouped_rentals.remove(grouped_rent)
                    break
        if(len(grouped_rentals) != 0):
            total_distance += distance_matrix_request(grouped_rentals)
        
        # send request to google, add to db, add to sum
        data = [rec for rec in data if rec not in filtered_data]

    for rental in data:
        total_distance +=distance_matrix_request(rental)
    return total_distance


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
