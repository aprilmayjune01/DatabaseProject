from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('flight_directory', __name__, template_folder='templates', url_prefix='/flight_directory')

### Helper functions ###

def execute_query(query, template, error_message):
    """
    Attempts to execute a query. If unsuccessful, renders an error page.
    """
    try:
        g.conn.execute(text(query))
        g.conn.commit()
    except Exception as e:
        print(e)
        return render_template(template, error=error_message)

def get_flight(flight_ID):
    """
    Returns a dictionary containing the flight's information.
    """

    select_query = f"""
    SELECT flight_ID, port_of_origin, destination, departure_time, flight_length, domestic, airline_ID 
    FROM flight
    WHERE flight_ID = '{flight_ID}'
    """

    context = dict()

    try: 
        cursor = g.conn.execute(text(select_query))
        result = cursor.fetchone()
        cursor.close()

        context = {
            "flight_ID": result[0],
            "port_of_origin": result[1],
            "destination": result[2],
            "departure_time": result[3],
            "flight_length": result[4],
            "domestic": result[5],
            "airline_ID": result[6],
        }

    except Exception as e:
        print(e)
        return None
    
    return context


### Routes ###

@bp.route("/")
def index():
    """
    Main page for flight_directory.
    Displays all flights.
    """

    select_query = """
    SELECT flight_ID, port_of_origin, destination, departure_time 
    FROM flight
    """

    flight_IDs = list()
    ports_of_origin = list()
    destinations = list() 
    departure_times = list()

    cursor = g.conn.execute(text(select_query))
    for result in cursor:
        flight_IDs.append(result[0])
        ports_of_origin.append(result[1])
        destinations.append(result[2])
        departure_times.append(result[3])
    cursor.close()

    context = {
        "flight_IDs": flight_IDs,
        "destinations": destinations,
        "ports_of_origin": ports_of_origin,
        "departure_times": departure_times,
    }

    return render_template("flight_directory.html", **context)

@bp.route("/view/<flight_ID>")
def view(flight_ID):
    """
    Displays a single flight.
    """
    context = get_flight(flight_ID)
    if context is None:
        return redirect(url_for("flight_directory.index"))
    
    return render_template("view_flight.html", **context)

@bp.route("/edit/<flight_ID>", methods=["GET", "POST"])
def edit(flight_ID):
    """
    Allows the user to edit a flight.
    """
    context = get_flight(flight_ID)
    if context is None:
        return redirect(url_for("flight_directory.index"))

    if request.method == "GET":
        return render_template("edit_flight.html", **context)


    if request.method == "POST":
        port_of_origin = request.form['port_of_origin']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        flight_length = request.form['flight_length']
        domestic = request.form['domestic']
        airline_ID = request.form['airline_ID']

        # Update the flight
        update_query = f"""
        UPDATE flight
        SET port_of_origin = '{port_of_origin}',
            destination = '{destination}',
            departure_time = '{departure_time}',
            flight_length = {flight_length},
            domestic = {domestic},
            airline_ID = {airline_ID}
        WHERE flight_ID = {flight_ID}
        """

        execute_query(update_query, "edit_flight.html", "Unable to edit flight. Make sure all fields are filled out correctly.")

        return redirect(url_for("flight_directory.index"))

    