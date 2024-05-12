from flask import Blueprint, jsonify
from FlightRadar24 import FlightRadar24API
from telegram import Bot

import os
from dotenv import load_dotenv


#Blueprint
api = Blueprint('api', __name__)

#Telegram Bot settingUP
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = Bot(token = TELEGRAM_BOT_TOKEN)

mustSeeWeb = []

#Send JSON to Telegram as Formatted message
def send_json_to_telegram(data):
    formatted_message = "🛫 **Vuelos Recientes** 🛬\n\n"
    for flight in data:
        formatted_message += f"**Vuelo:** {flight['flight']}\n"
        formatted_message += f"**Callsign:** {flight['callsign']}\n"
        formatted_message += f"**Destino:** {flight['destination']}\n\n"
    
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=formatted_message, parse_mode='Markdown')


#Get flights and send them to Telegram
def get_and_send_flights():
    types = ["A330", "A340", "A350", "A380", "747", "757", "767", "777", "787"]
    mustSee = []
    fr = FlightRadar24API()
    airport = fr.get_airport("MAD")

    if not airport:
        return jsonify(message="Airport not found"), 404

    bounds = fr.get_bounds_by_point(latitude=airport.latitude, longitude=airport.longitude, radius=5500)
    flights = fr.get_flights(bounds=bounds)
    
    for flight in flights:
        flight_details = fr.get_flight_details(flight=flight)
        flight.set_flight_details(flight_details=flight_details)
        
        for aircraft_type in types:
            if aircraft_type in flight.aircraft_model and flight.origin_airport_name == airport.name:
                mustSee.append({
                    "flight": flight.aircraft_model,
                    "callsign": flight.callsign,
                    "destination": flight.destination_airport_name
                })

    json_data = mustSee
    mustSeeWeb.append(mustSee)
    
    print(json_data)
    
    send_json_to_telegram(json_data)
    
get_and_send_flights()

#Main route using ICAO code to search for airport
@api.route('/flights/')
def get_flights():
    return jsonify(mustSeeWeb)