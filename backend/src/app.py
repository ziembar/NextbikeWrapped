import time
from flask import Flask, request, jsonify
import os
from decouple import config
from datetime import datetime
from google_requests import static_map_request
import defs
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(app)
   
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
            cookie, name = defs.get_cookie(phone, pin)
            return jsonify({"cookie": cookie, "name": name, "code": 200})
        except:
            return "Invalid login credentials", 401
        

    @app.route('/api/summary', methods=['GET', 'POST'])
    def get_data():
        
        try:
            start = int(request.json['start'])
            end = int(request.json['end'])
            cookie = str(request.json['cookie'])

        except:
            return "Invalid request", 400

        current_time = int(datetime.now().timestamp())

        if start is None or start > current_time or end is None or end < start :
            return "Provide a valid time range!", 400

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
            total_time, total_money, total_co2, total_calories = defs.total_time_money_co2_calories(filtered_data)
            total_rides = len(filtered_data)
            g_data = defs.group_rentals(filtered_data)

            top_rides = defs.top_frequent_rides(g_data)
            total_distance = defs.total_distance(g_data)
            b64map = static_map_request(g_data)
        except Exception as e:
            return str(e), 500

        return jsonify({
            "total_rides": total_rides,
            "total_time": total_time,
            "total_money": total_money,
            "total_co2": total_co2,
            "total_calories": total_calories,
            "top_rides": top_rides,
            "total_distance": total_distance,
            "map": b64map,
            "no_data": False
        })

    # TODO: add logs to error handling
    return app