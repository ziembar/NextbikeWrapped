import time
from decouple import config
from db_actions import *
from Models import getDriver, getMongoClient
import requests
import json
from google_requests import *
import jwt
from urllib.parse import urlencode


def get_api_key():
    # req = requests.get("https://webview.nextbike.net/getAPIKey.json", headers={ "user-agent": "nextbike-av4"})
    # if req.ok:
    #     return req.json()['apiKey']

    ## WHY NEXTBIKE WHY
    return 'OobHOQY4g9UuOT1S'

def get_login_key(phone, pin):
    api_key = get_api_key()
    url = "https://api.nextbike.net/api/login.json"

    data = {
        "mobile": phone,
        "pin": pin,
        "api_key": api_key,
        'show_errors': 1
    }

    response = requests.post(url, data=data)

    if 'error' in response.json():
        raise Exception(f"Login failed with code {response.json()['error']['code']}. Message: {response.json()['error']['message']}")

    token = response.json()['user']['appform_auth_token']
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    exp = decoded_token.get("exp")

    return response.json()['user']['loginkey'], response.json()['user']['screen_name'], exp

def resetPin(phone):
    api_key = get_api_key()

    if not phone.startswith('+'):
        phone = '+' + phone
    params = {
        "api_key": api_key,
        "mobile": phone
    }
    headers = {
        'Accept-Encoding': 'gzip'
    }

    url = f"https://api.nextbike.net/api/v1.1/pinRecover.json?{urlencode(params)}"

    response = requests.post(url, headers)
    return response.status_code


def get_events(loginkey):
    api_key = get_api_key()
    url = f"https://api.nextbike.net/api/v1.1/list.json?api_key={api_key}&loginkey={loginkey}&limit=none"
    api_key = requests.get("https://webview.nextbike.net/getAPIKey.json").json()['apiKey']

    headers = {
        'Accept-Encoding': 'gzip',
        'Connection': 'Keep-Alive',
        'User-Agent': 'user-agent": "nextbike-av4'
    }

    response = requests.get(url, headers=headers)

    return response.json()


def filter_by_season(data, start, end):
    filtered_data = []
    for rental in data['account']['items']:
        if rental['node'] != "rental":
            continue
        start_time = rental['start_time']
        end_time = rental['end_time']
        if start_time >= start and end_time <= end:
            filtered_data.append(rental)
    return filtered_data


def filter_last_week(data):
    filtered_data = []
    for rental in data['account']['items']:
        start_time = rental['start_time']
        if start_time >= time.time() - 60*60*24*7:
            filtered_data.append(rental)
    return filtered_data

def get_all_stations():
    response = requests.get("https://api.nextbike.net/maps/nextbike-live.json")
    return response.json()



def filter_same_station(data):
    filtered_data = []
    for rental in data:
        start_station = rental['start_place']
        end_station = rental['end_place']
        if start_station != end_station and rental['end_place_lng'] !=0 and rental['end_place_lat'] != 0 and rental['start_place_lng'] !=0 and rental['start_place_lat'] != 0:
            filtered_data.append(rental)
    return filtered_data


def top_frequent_rides(g_data):
    sorted_rides = sorted(g_data, key=lambda x: x['amount'], reverse=True)
    top_rides = sorted_rides[:3]

    new_top_rides = []
    for rental in top_rides:
        if rental['start_place_name'] and rental['end_place_name']:
            start_name = rental['start_place_name']
            end_name = rental['end_place_name']
            new_top_rides.append([min(start_name, end_name), max(start_name, end_name), rental['amount']])
    return new_top_rides


def total_time_cost_gain(data):
    total_time = 0
    total_cost = 0
    total_gain = 0

    for rental in data:
        duration = rental['end_time'] - rental['start_time']
        total_time += duration
        total_cost += rental['price']
        if rental['price_service'] < 0:
            total_gain -= rental['price_service']
        else:
            total_cost += rental['price_service']



    return round(total_time/60,1), round(total_cost/100, 2), round(total_gain/100, 2)




def group_rentals(data):
    grouped_rentals = []
    for rental in data:
        start_station = rental['start_place']
        end_station = rental['end_place']
        found = False
        for existing_rental in grouped_rentals:
            if ((existing_rental['start_place'] == start_station and existing_rental['end_place'] == end_station) or (existing_rental['start_place'] == end_station and existing_rental['end_place'] == start_station)):
                existing_rental['amount'] += 1
                found = True
                break
        if not found:
            rental['amount'] = 1
            grouped_rentals.append(rental)
    return grouped_rentals





def filter_by_station(data, station):
    filtered_data = []
    for rental in data:
        if (rental['start_place'] == station or rental['end_place'] == station):
            if rental['end_place'] == station:
                rental['start_place'], rental['end_place'] = rental['end_place'], rental['start_place']
                rental['start_place_lat'], rental['end_place_lat'] = rental['end_place_lat'], rental['start_place_lat']
                rental['start_place_lng'], rental['end_place_lng'] = rental['end_place_lng'], rental['start_place_lng']
                rental['start_place_name'], rental['end_place_name'] = rental['end_place_name'], rental['start_place_name']
                rental['start_place_type'], rental['end_place_type'] = rental['end_place_type'], rental['start_place_type']
                rental['reversed'] = True
            filtered_data.append(rental)
    return filtered_data

def total_distance(data):
    # TODO: fix two-way distance calculation, add longest ride
    total_distance = 0
    longest_ride = {"distance": 0, "rent": None}
    fastest_ride = {"velocity": 0, "rent": None}

    stations = {}
    for rental in data:
        start_station = rental['start_place']
        end_station = rental['end_place']
        amount = rental['amount']

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

        db_result = find_station_by_uid(getDriver(), station[0])

        filtered_data_copy = filtered_data.copy()
        for grouped_rent in filtered_data_copy:
            for record in db_result:

                # print("pulled from db: ", record['s'].get('name'),"<--->" , record['d'].get('name'))
                # print("comparing ['d'] with: ", grouped_rent['end_place_name'])
                if record['d'].get('uid') == grouped_rent['end_place']:
                    # print("its a match!")
                    total_distance += record['r'].get('distance') * grouped_rent['amount']

                    if longest_ride['distance'] < record['r'].get('distance'):
                        longest_ride['distance'] = record['r'].get('distance')
                        longest_ride['rent'] = grouped_rent

                    if fastest_ride['velocity'] < (record['r'].get('distance')/1000) / ((grouped_rent['end_time'] - grouped_rent['start_time'])/3600):
                        fastest_ride['velocity'] = (record['r'].get('distance')/1000) / ((grouped_rent['end_time'] - grouped_rent['start_time'])/3600)
                        fastest_ride['rent'] = grouped_rent
                    filtered_data.remove(grouped_rent)
                    break
        if(len(filtered_data) != 0):
            # Divide the command into multiple calls with a maximum of 25 elements in the filtered_data array
            chunk_size = 25
            num_chunks = len(filtered_data) // chunk_size + 1

            for i in range(num_chunks):
                start_index = i * chunk_size
                end_index = min((i + 1) * chunk_size, len(filtered_data))
                chunk = filtered_data[start_index:end_index]
                total_distance += distance_matrix_request(chunk, longest_ride, fastest_ride)
        
        # send request to google, add to db, add to sum
        data = [rec for rec in data if rec not in filtered_data_copy]

    for rental in data:
        total_distance +=distance_matrix_request([rental], longest_ride, fastest_ride)

    if longest_ride.get('reversed'):
        top_ride = {"start_place": longest_ride['rent']['end_place_name'], "end_place": longest_ride['rent']['start_place_name'], "distance": longest_ride['distance'], "time": longest_ride['rent']['end_time'] - longest_ride['rent']['start_time']}
    else:
        longest_ride = {"start_place": longest_ride['rent']['start_place_name'], "end_place": longest_ride['rent']['end_place_name'], "distance": longest_ride['distance'], "time": longest_ride['rent']['end_time'] - longest_ride['rent']['start_time']}
    
    if fastest_ride.get('reversed'):
        top_ride = {"start_place": fastest_ride['rent']['end_place_name'], "end_place": fastest_ride['rent']['start_place_name'], "velocity": fastest_ride['velocity']}
    else:
        fastest_ride = {"start_place": fastest_ride['rent']['start_place_name'], "end_place": fastest_ride['rent']['end_place_name'], "velocity": fastest_ride['velocity']}
    
    return total_distance, longest_ride, fastest_ride




def write_summary(data):
    return write_summary_db(getMongoClient(), data)

def read_summary(objectId):
    return read_summary_db(getMongoClient(), objectId)

def get_cookie(phone, pin):
        url = "https://account.nextbike.pl/api/login"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
        }
        data = {
            "phone": phone,
            "pin": pin,
            "city": "vw",
            "country_code":"48"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())
        name = response.json().get("login")

        return response.headers['set-cookie'], name