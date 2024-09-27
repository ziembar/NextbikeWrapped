import time
from flask import Flask, request, jsonify
import os
from decouple import config
from datetime import datetime
from defs import *
from flask_cors import CORS
import sys
import pickle




app = Flask(__name__)
cors = CORS(app)

@app.route('/api/test', methods=['POST', 'GET'])
def hello():
    phone = str(request.json['phone'])
    pin = str(request.json['pin'])
    cookie, name = get_cookie(phone, pin)
    return jsonify({"cookie": cookie,"name": name})



@app.route('/api/login', methods=['POST', 'GET'])
def login():
    try:
        phone = str(request.json['phone'])
        pin = request.json['pin']

    except:
        return jsonify({"statusText": "Invalid request"}), 401


    try:
        login_key, name, exp = get_login_key(phone, pin)
    except:
        return jsonify({"statusText": "Invalid login credentials"}), 401
    return jsonify({"cookie": login_key, "name": name, "exp": exp, "code": 200}), 200
    

@app.route('/api/summary', methods=['GET', 'POST'])
def get_data():

    try:
        summary_id = str(request.json['id'])
        if summary_id:
            try:
                res = read_summary(summary_id)
                if res:
                    return jsonify(res), 200
                else:
                    return jsonify({"statusText": "Summary not found"}), 404

            except Exception as e:
                    return jsonify({"statusText": "Something went wrong..."}), 500

    except:
        pass

    
    try:
        cookie = str(request.json['cookie'])
        name = str(request.json['name'])

    except:
        return jsonify({"statusText": "Invalid request"}), 400

    current_time = int(datetime.now().timestamp())
    season_name = str(request.json['season_name'])

    try:
        start = int(request.json['start'])
        end = int(request.json['end'])

    except:
        start = 0
        end = current_time


    try:
        events = get_events(cookie)
        if 'error' in events:
            raise Exception("Something went wrong, try logging again")
    except Exception as e: 
            return jsonify({"statusText": "Something went wrong..."}), 500


    
    try:

        filtered_data = filter_by_season(events, start, end)
        if(len(filtered_data) == 0):
            return jsonify({"no_data": True}), 200
        total_time, total_cost, total_gain = total_time_cost_gain(filtered_data)
        total_rides = len(filtered_data)

        filtered_deduped_data = filter_same_station(filtered_data)

        g_data = group_rentals(filtered_deduped_data)

        top_rides = top_frequent_rides(g_data)
        distance, longest_ride, fastest_ride = total_distance(g_data)
        b64map = static_map_request(g_data)
    except Exception as e:
        return jsonify({"statusText": "Something went wrong..."}), 500


    res = {
        "total_rides": total_rides,
        "total_time": total_time,
        "total_cost": total_cost,
        "total_gain": total_gain,
        "top_rides": top_rides,
        "total_distance": distance,
        "longest_ride": longest_ride,
        "fastest_ride": fastest_ride,
        "map": b64map,
        "name": name,
        "season_name": season_name,
    }

    summary_id = write_summary(res.copy())

    res['id'] = str(summary_id)

    return jsonify(res), 200