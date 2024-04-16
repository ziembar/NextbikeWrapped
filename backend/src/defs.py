import time
from decouple import config
import db_actions
from Models import getDriver
import requests
import json
from google_requests import distance_matrix_request



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


def top_frequent_rides(g_data):
    sorted_rides = sorted(g_data, key=lambda x: x['amount'], reverse=True)
    top_rides = sorted_rides[:3]

    new_top_rides = []
    for rental in top_rides:
        if rental['startPlace']['name'] and rental['endPlace']['name']:
            start_name = rental['startPlace']['name']
            end_name = rental['endPlace']['name']
            new_top_rides.append([min(start_name, end_name), max(start_name, end_name), rental['amount']])
    return new_top_rides


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
            if ((existing_rental['startPlace']['name'] == start_station and existing_rental['endPlace']['name'] == end_station) or (existing_rental['startPlace']['name'] == end_station and existing_rental['endPlace']['name'] == start_station)):
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
        amount = rental['amount']

        if(start_station == None or end_station == None):
            continue
        if start_station in stations:
            stations[start_station] += amount
        else:
            stations[start_station] = amount
        if end_station in stations:
            stations[end_station] += amount
        else:
            stations[end_station] = amount
    sorted_stations = sorted(stations.items(), key=lambda x: x[1], reverse=True)

    for station in sorted_stations:
        # print("--------STATION: ", station, "-------")
        if len(data) == 0:
            break
        filtered_data = filter_by_station(data, station[0])
        if(len(filtered_data) == 0):
            continue

        db_result = db_actions.find_station_by_coordinates(getDriver(), filtered_data[0]['startPlace']['lat'], filtered_data[0]['startPlace']['lng'])

        filtered_data_copy = filtered_data.copy()
        for grouped_rent in filtered_data_copy:
            for record in db_result:

                # print("pulled from db: ", record['s'].get('name'),"<--->" , record['d'].get('name'))
                # print("comparing ['d'] with: ", grouped_rent['endPlace']['name'])
                if record['d'].get('name') == grouped_rent['endPlace']['name']:
                    # print("its a match!")
                    total_distance += record['r'].get('distance') * grouped_rent['amount']
                    filtered_data.remove(grouped_rent)
                    break
        if(len(filtered_data) != 0):
            total_distance += distance_matrix_request(filtered_data)
        
        # send request to google, add to db, add to sum
        data = [rec for rec in data if rec not in filtered_data_copy]

    for rental in data:
        total_distance +=distance_matrix_request([rental])
    return total_distance


