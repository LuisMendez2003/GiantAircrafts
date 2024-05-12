from flask import Blueprint, jsonify
from FlightRadar24 import FlightRadar24API

#Blueprint
api = Blueprint('api', __name__)

#Main route using ICAO code to search for airport
@api.route('/flights/<string:airport_code>')
def get_flights(airport_code):
    types = ["A330", "A340", "A350", "A380", "747", "757", "767", "777", "787"]
    mustSee = []
    fr = FlightRadar24API()
    airport = fr.get_airport(airport_code)

    if not airport:
        return jsonify(message="Airport not found"), 404

    bounds = fr.get_bounds_by_point(latitude = airport.latitude, longitude = airport.longitude, radius = 5500)
    flights = fr.get_flights(bounds = bounds)
    
    for flight in flights:
        flight_details = fr.get_flight_details(flight = flight)
        flight.set_flight_details(flight_details = flight_details)
        
        for aircraft_type in types:
            if aircraft_type in flight.aircraft_model and flight.origin_airport_name == airport.name:
                mustSee.append({
                    "flight": flight.aircraft_model,
                    "callsign": flight.callsign,
                    "destination": flight.destination_airport_name
                })

    return jsonify(mustSee)