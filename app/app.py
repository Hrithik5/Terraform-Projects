import boto3
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ERGAST_API_URL = "http://ergast.com/api/f1"
CACHE_TTL = 3600  # 1 hour cache

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('f1-stats-cache')

def get_cached_data(endpoint):
    try:
        response = table.get_item(
            Key={
                'endpoint': endpoint,
                'timestamp': int(time.time())
            }
        )
        if 'Item' in response:
            item = response['Item']
            if item['expiry_time'] > int(time.time()):
                return item['data']
    except Exception as e:
        print(f"Cache error: {e}")
    return None

def cache_data(endpoint, data):
    try:
        table.put_item(
            Item={
                'endpoint': endpoint,
                'timestamp': int(time.time()),
                'data': data,
                'expiry_time': int(time.time()) + CACHE_TTL
            }
        )
    except Exception as e:
        print(f"Cache error: {e}")

@app.route('/api/drivers')
def get_drivers():
    cached_data = get_cached_data('drivers')
    if cached_data:
        return jsonify(cached_data)

    response = requests.get(f"{ERGAST_API_URL}/2024/drivers.json")
    if response.status_code == 200:
        drivers_data = response.json()['MRData']['DriverTable']['Drivers']
        formatted_drivers = [{
            'driver_number': driver.get('permanentNumber', 'N/A'),
            'full_name': f"{driver.get('givenName', '')} {driver.get('familyName', '')}",
            'nationality': driver.get('nationality', 'Unknown'),
            'code': driver.get('code', 'N/A'),
            'date_of_birth': driver.get('dateOfBirth', 'N/A'),
            'wiki_url': driver.get('url', '#'),
            'image_url': f"https://cdn.formula1.com/content/dam/fom-website/drivers/{driver.get('familyName').lower()}.jpg"
        } for driver in drivers_data]
        
        cache_data('drivers', formatted_drivers)
        return jsonify(formatted_drivers)
    return jsonify({'error': 'Unable to fetch drivers data'}), 500

@app.route('/api/constructors')
def get_constructors():
    cached_data = get_cached_data('constructors')
    if cached_data:
        return jsonify(cached_data)

    response = requests.get(f"{ERGAST_API_URL}/2024/constructors.json")
    if response.status_code == 200:
        constructors = response.json()['MRData']['ConstructorTable']['Constructors']
        formatted_constructors = [{
            'name': constructor['name'],
            'nationality': constructor['nationality'],
            'wiki_url': constructor['url'],
            'image_url': f"https://cdn.formula1.com/content/dam/fom-website/teams/{constructor['name'].lower().replace(' ', '_')}.jpg"
        } for constructor in constructors]
        
        cache_data('constructors', formatted_constructors)
        return jsonify(formatted_constructors)
    return jsonify({'error': 'Unable to fetch constructors data'}), 500

@app.route('/api/driver-standings/all-time')
def get_all_time_driver_standings():
    cached_data = get_cached_data('driver-standings')
    if cached_data:
        return jsonify(cached_data)

    response = requests.get(f"{ERGAST_API_URL}/driverStandings/1.json?limit=100")
    if response.status_code == 200:
        standings = response.json()['MRData']['StandingsTable']['StandingsLists']
        formatted_standings = [{
            'year': standing['season'],
            'driver': f"{standing['DriverStandings'][0]['Driver']['givenName']} {standing['DriverStandings'][0]['Driver']['familyName']}",
            'constructor': standing['DriverStandings'][0]['Constructors'][0]['name'],
            'points': standing['DriverStandings'][0]['points'],
            'wins': standing['DriverStandings'][0]['wins']
        } for standing in standings]
        
        cache_data('driver-standings', formatted_standings)
        return jsonify(formatted_standings)
    return jsonify({'error': 'Unable to fetch historical standings data'}), 500

@app.route('/api/constructor-standings/all-time')
def get_all_time_constructor_standings():
    cached_data = get_cached_data('constructor-standings')
    if cached_data:
        return jsonify(cached_data)

    response = requests.get(f"{ERGAST_API_URL}/constructorStandings/1.json?limit=100")
    if response.status_code == 200:
        standings = response.json()['MRData']['StandingsTable']['StandingsLists']
        formatted_standings = [{
            'year': standing['season'],
            'constructor': standing['ConstructorStandings'][0]['Constructor']['name'],
            'nationality': standing['ConstructorStandings'][0]['Constructor']['nationality'],
            'points': standing['ConstructorStandings'][0]['points'],
            'wins': standing['ConstructorStandings'][0]['wins']
        } for standing in standings]
        
        cache_data('constructor-standings', formatted_standings)
        return jsonify(formatted_standings)
    return jsonify({'error': 'Unable to fetch constructor standings data'}), 500

@app.route('/api/current-season')
def get_current_season():
    cached_data = get_cached_data('current-season')
    if cached_data:
        return jsonify(cached_data)

    response = requests.get(f"{ERGAST_API_URL}/2024.json")
    if response.status_code == 200:
        races = response.json()['MRData']['RaceTable']['Races']
        formatted_races = [{
            'round': race['round'],
            'race_name': race['raceName'],
            'circuit': race['Circuit']['circuitName'],
            'location': f"{race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}",
            'date': race['date'],
            'time': race.get('time', 'TBA'),
            'first_practice': race.get('FirstPractice', {}),
            'second_practice': race.get('SecondPractice', {}),
            'third_practice': race.get('ThirdPractice', {}),
            'qualifying': race.get('Qualifying', {}),
            'sprint': race.get('Sprint', {})
        } for race in races]
        
        cache_data('current-season', formatted_races)
        return jsonify(formatted_races)
    return jsonify({'error': 'Unable to fetch season calendar'}), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)