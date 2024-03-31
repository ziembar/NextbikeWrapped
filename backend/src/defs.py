from flask import Flask, request, jsonify
from decouple import config
import db_actions
import datetime
from Models import getDriver, Station
import requests
import json


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

        return response.headers['set-cookie']


def get_events(cookie):
    url = "https://account.nextbike.pl/api/events"
    cookies = {
        "Cookie": cookie,
    }
    response = requests.get(url, headers=cookies, cookies=cookies)

    return response.json()


def filter_by_season(data, season):
    filtered_data = []
    for rental in data['rentals']:
        start_time = datetime.datetime.fromtimestamp(rental['startTime']).year
        end_time = datetime.datetime.fromtimestamp(rental['endTime']).year
        if start_time == season and end_time == season:
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


def total_time(data):
    total_time = 0
    for rental in data:
        duration = rental['endTime'] - rental['startTime']
        total_time += duration
    return round(total_time/60,1)


def money_spent(data):
    total_cost = 0
    for rental in data:
        total_cost += rental['price']
    return total_cost/100


def total_co2_saved(data):
    total_co2 = 0
    for rental in data:
        co2_saved = rental['co2']
        total_co2 += co2_saved
    return total_co2

def total_rides(data):
    return len(data)


def filter_by_station(data, station):
    filtered_data = []
    for rental in data:
        start_station = rental['startPlace']['name']
        end_station = rental['endPlace']['name']
        if start_station == end_station:
            continue
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
        
        if len(data) == 0:
            break
        filtered_data = filter_by_station(data, station[0])
        if(len(filtered_data) == 0):
            continue
        grouped_rentals =  group_rentals(filtered_data)
        db_result = db_actions.find_station_by_coordinates(getDriver(), grouped_rentals[0]['startPlace']['lat'], grouped_rentals[0]['startPlace']['lng'])

        for grouped_rent in grouped_rentals:
            for record in db_result:
                if record['d'].get('name') == grouped_rent['endPlace']['name']:
                    total_distance += record['r'].get('distance') * grouped_rent['amount']
                    grouped_rentals.remove(grouped_rent)
                    break

        
        # send request to google, add to db, add to sum
        data = [rec for rec in data if rec not in filtered_data]

    for rental in data:
        # send request for bikes left/rented not from stations, add to sum
        print("no station rental", rental)
    return total_distance





















cookie = get_cookie(config('TEST_NUMBER'), config('TEST_PIN'))

rents = get_events(cookie)

frents = filter_by_season(rents, 2024)

print(total_distance(frents))



# # print(frents)
# print(defs.money_spent(frents))




# a=db_actions.find_station_by_coordinates(getDriver(), "52.290974", "20.929556")
# print(a)
db_actions.add_distance_relation(getDriver(), 52.131093, 21.06548, 52.133264, 21.074796, 1000, 5)

# a=db_actions.find_station_by_coordinates(getDriver(), "52.290974", "20.929556")
# print(a[1]['s'].get('number'))
# for v in a.values():
#     print(v, '\n')

# getDriver().close()

