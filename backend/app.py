import time
from flask import Flask, request, jsonify
import os
from decouple import config
from datetime import datetime
import defs
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": [config('FRONTEND_URL')]}})
   
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/api/login', methods=['POST', 'GET'])
    def login():
        try:
            phone = str(request.json['phone'])
            pin = request.json['pin']

            phone = "48" + phone
      
        except:
            return "Invalid request", 400

        try:
            login_key, name, exp = defs.get_login_key(phone, pin)
            print(login_key, name)
            return jsonify({"cookie": login_key, "name": name, "exp": exp, "code": 200}), 200
        except:
            return "Invalid login credentials", 401
        

    @app.route('/api/summary', methods=['GET', 'POST'])
    def get_data():
        
        try:
            cookie = str(request.json['cookie'])

        except:
            return "Invalid request", 400

        current_time = int(datetime.now().timestamp())
        try:
            start = int(request.json['start'])
            end = int(request.json['end'])
        except:
            start = 0
            end = current_time


        try:
            events = defs.get_events(cookie)
            if 'error' in events:
                raise Exception("Something went wrong, try logging again")
        except Exception as e: 
            return str(e), 500
        
        try:

            filtered_data = defs.filter_by_season(events, start, end)
            if(len(filtered_data) == 0):
                return jsonify({"no_data": True}), 200
            total_time, total_cost, total_gain = defs.total_time_cost_gain(filtered_data)
            total_rides = len(filtered_data)

            filtered_deduped_data = defs.filter_same_station(filtered_data)

            g_data = defs.group_rentals(filtered_deduped_data)

            top_rides = defs.top_frequent_rides(g_data)
            total_distance, longest_ride = defs.total_distance(g_data)
            b64map = static_map_request(g_data)
        except Exception as e:
            return str(e), 500

        return jsonify({
            "total_rides": total_rides,
            "total_time": total_time,
            "total_cost": total_cost,
            "total_gain": total_gain,
            "top_rides": top_rides,
            "total_distance": total_distance,
            "longest_ride": longest_ride,
            "map": b64map,
            "no_data": False
        })

    # TODO: add logs to error handling
    return app