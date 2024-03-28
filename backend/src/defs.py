from flask import Flask, request, jsonify
import datetime
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

def get_all_stations():
    response = requests.get("https://api.nextbike.net/maps/nextbike-live.json?city=812")
    return response.json()['countries'][0]['cities'][0]['places']


def total_rides(data):
    return len(data)

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