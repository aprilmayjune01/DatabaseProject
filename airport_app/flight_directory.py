from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('flight_directory', __name__, template_folder='templates', url_prefix='/flight_directory')

@bp.route("/")
def index():
    """
    Main page for flight_directory.
    Displays all flights.
    """

    select_query = """
    SELECT * FROM flight
    """

    

    flight_IDs = list()
    destinations = list() 
    port_of_origins = list()
    departure_times = list()
    flight_lengths = list
    domestic = list()
    airline_ids = list() 



    cursor = g.conn.execute(text(select_query))
    for result in cursor:
        

        flight_IDs.append(result[0])
        destinations.append(result[1])
        port_of_origins.append(result[2])
        departure_times.append(result[3])
        flight_lengths.append(result[4])
        domestic.append(result[5])
        airline_ids.append(result[6])


    cursor.close()

    context = {
        "flight_IDs": flight_IDs,
        "destinations": destinations,
        "port_of_origins": port_of_origins,
        "departure_times": departure_times,
        "flight_lengths": flight_lengths,
        "domestic": domestic,
        "airline_ids": airline_ids,
    }

    return render_template("flight_directory.html", **context)
