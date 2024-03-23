import os
from settings import settings
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

    print(response.status_code)
    return response.json()


def filter_by_season(data, season):
    filtered_data = []
    for rental in data['rentals']:
        start_time = datetime.datetime.fromtimestamp(rental['startTime']).year
        end_time = datetime.datetime.fromtimestamp(rental['endTime']).year
        if start_time == season and end_time == season:
            filtered_data.append(rental)
    return filtered_data