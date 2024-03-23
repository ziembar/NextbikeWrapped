import os
from settings import settings
from flask import Flask, request, jsonify
import defs

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('GOOGLE_API_KEY'),
    )
   
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        try:
            phone = request.json['phone']
            pin = request.json['pin']
        except:
            return jsonify({"error": "Invalid request", "code": 400})

        try:
            cookie = defs.get_cookie(phone, pin)
        except:
            return jsonify({"error": "Invalid login credentials", "code": 401})
        
        try:
            events = defs.get_events(cookie)
        except: return jsonify({"error": "Something went wrong, try again", "code": 500})

        return events

    return app