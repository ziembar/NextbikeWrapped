from flask import Flask, request, jsonify
import defs
import os
from decouple import config
from datetime import datetime



def create_app():
    app = Flask(__name__)
   
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/api/login', methods=['POST'])
    def login():
        print(app.config.get('GOOGLE_API_KEY'))
        try:
            phone = request.json['phone']
            pin = request.json['pin']
        except:
            return jsonify({"error": "Invalid request", "code": 400})

        try:
            return jsonify({"cookie": defs.get_cookie(phone, pin)})
        except:
            return jsonify({"error": "Invalid login credentials", "code": 401})
        

    @app.route('/api/summary', methods=['GET', 'POST'])
    def get_data():
        season = request.args.get('season')
        cookie = request.json['cookie']

        current_year = datetime.now().year

        if season is None or not season.isdigit() or int(season) < 2015 or int(season) > current_year:
            return jsonify({"error": "Provide a valid season year!", "code": 40})

        try:
            events = defs.get_events(cookie)
        except: 
            return jsonify({"error": "Something went wrong, try again", "code": 500})
        
        filtered_data = defs.filter_by_season(events, int(season))


        






        return jsonify({"data": filtered_data})

    return app