from flask import Flask, request, jsonify
import os
from decouple import config
from datetime import datetime
import defs
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(app)
   
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/api/login', methods=['POST', 'GET', 'OPTIONS'])
    def login():
        try:
            phone = str(request.json['phone'])
            pin = request.json['pin']

            phone = "48" + phone
      
        except:
            return jsonify({"error": "Invalid request", "code": 400})

        try:
            cookie, name = defs.get_cookie(phone, pin)
            return jsonify({"cookie": cookie, "name": name, "code": 200})
        except:
            return jsonify({"error": "Invalid login credentials", "code": 401})
        

    @app.route('/api/summary', methods=['GET', 'POST', 'OPTIONS'])
    def get_data():
        try:
            time = float(request.json['time'])
            cookie = request.json['cookie']
        except:
            return jsonify({"error": "Invalid request", "code": 400})

        current_time = datetime.now().timestamp()

        if time is None or time > current_time:
            return jsonify({"error": "Provide a valid season year!", "code": 400})

        try:
            events = defs.get_events(cookie)
            if 'error' in events:
                raise Exception("Something went wrong, try logging again")
        except Exception as e: 
            return jsonify({"error": str(e), "code": 500})
        
        filtered_data = defs.filter_by_season(events, time)

        total_time, total_money, total_co2, total_calories = defs.total_time_money_co2_calories(filtered_data)
        return jsonify({
            "total_rides": len(filtered_data),
            "total_time": total_time,
            "total_money": total_money,
            "total_co2": total_co2,
            "total_calories": total_calories,
            "top_rides": defs.top_frequent_rides(filtered_data),
            "total_distance": defs.total_distance(filtered_data),
        })

    return app