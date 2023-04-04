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

def get_flown_with_vessel(flight_ID):
    """
    """

    context = dict()

    select_query = f"""
    SELECT fv.aircraft_ID, fv.flight_ID, a.model
    FROM flown_with_vessel fv
    JOIN aircraft a ON a.vessel_ID = fv.aircraft_ID
    WHERE fv.flight_ID = '{flight_ID}'
    """

    try: 
        cursor = g.conn.execute(text(select_query))
        result = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print(e)
        return None

    if result is not None:
        context = {
            "aircraft_ID": result[0],
            "flight_ID": result[1],
            "model": result[2],
        }

    return context


    

def get_airlines():
    """
    Returns a dictionary containing all airlines.
    """
    select_query = """
    SELECT airline_ID, airline_name
    FROM airline
    """

    airline_IDs = list()
    airline_names = list()

    try:
        cursor = g.conn.execute(text(select_query))
        for result in cursor:
            airline_IDs.append(result[0])
            airline_names.append(result[1])
        cursor.close()
    except Exception as e:
        print(e)
        return None
    
    context = {
        "airline_IDs": airline_IDs,
        "airline_names": airline_names,
    }

    return context

def get_airline(airline_ID):
    """
    Returns a dictionary containing the airline's information.
    """

    select_query = f"""
    SELECT airline_ID, airline_name
    FROM airline
    WHERE airline_ID = '{airline_ID}'
    """

    context = dict()

    try: 
        cursor = g.conn.execute(text(select_query))
        result = cursor.fetchone()
        cursor.close()

        context = {
            "airline_ID": result[0],
            "airline_name": result[1]
        }

    except Exception as e:
        print(e)
        return None
    
    return context

def get_max_flight_ID():
    """
    Returns the maximum flight_ID in the database.
    """
    select_query = """
    SELECT flight_ID
    FROM flight
    """

    max_flight_ID = 0

    try:
        cursor = g.conn.execute(text(select_query))
        for result in cursor:
            if int(result[0]) > max_flight_ID:
                max_flight_ID = int(result[0])
        cursor.close()
    except Exception as e:
        print(e)
        return None
    
    return max_flight_ID


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
    if context is None or len(context) == 0:
        return redirect(url_for("flight_directory.index"))
    
    airline = get_airline(context["airline_ID"])
    if airline is None or len(airline) == 0:
        return redirect(url_for("flight_directory.index", error="Unable to view flight. Please try again."))

    flown_with_vessel = get_flown_with_vessel(flight_ID)
    if flown_with_vessel is None:
        return redirect(url_for("flight_directory.index"))
    
    context.update(airline)
    context.update(flown_with_vessel)
    
    return render_template("view_flight.html", **context)

@bp.route("/edit/<flight_ID>", methods=["GET", "POST"])
def edit(flight_ID):
    """
    Allows the user to edit a flight.
    """
    error_message = "Unable to edit flight. Make sure all fields are filled out correctly."
    error_template = "edit_flight.html"

    context = get_flight(flight_ID)
    if context is None or len(context) == 0:
        return redirect(url_for("flight_directory.index"))
    
    airline_data = get_airlines()
    if airline_data is None or len(airline_data["airline_IDs"]) == 0:
        return render_template(error_template, error="Unable to edit flight. Please try again.")
    else: 
        context.update(airline_data)
    

    if request.method == "GET":
        return render_template("edit_flight.html", **context)


    if request.method == "POST":
        port_of_origin = request.form['port_of_origin']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        flight_length = request.form['flight_length']
        if 'domestic' in request.form:
            domestic = True
        else:
            domestic = False
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
        WHERE flight_ID = '{flight_ID}'
        """

        execute_query(update_query, "edit_flight.html", "Unable to edit flight. Make sure all fields are filled out correctly.")

        return redirect(url_for("flight_directory.view", flight_ID=flight_ID))

@bp.route("/delete/<flight_ID>")
def delete(flight_ID):
    """
    Allows the user to delete a flight.
    """
    context = get_flight(flight_ID)
    if context is None:
        return redirect(url_for("flight_directory.index"))

    delete_query = f"""
    DELETE FROM flight
    WHERE flight_ID = '{flight_ID}'
    """

    execute_query(delete_query, "view_flight.html", "Unable to delete flight.")

    return redirect(url_for("flight_directory.index"))

@bp.route("/create", methods=["GET", "POST"])
def create():
    """
    Allows the user to create a flight.
    """
    # Default error data
    error_message = "Unable to create flight. Make sure all fields are filled out correctly."
    error_template = "create_flight.html"

    # Get airline data
    airline_data = get_airlines()
    if airline_data is None or len(airline_data["airline_IDs"]) == 0:
        return render_template(error_template, error="Unable to create flight. Please try again.")
    else: 
        context = airline_data

    if request.method == "GET":
        return render_template("create_flight.html", **context)

    if request.method == "POST":
        port_of_origin = request.form['port_of_origin']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        flight_length = request.form['flight_length']
        if 'domestic' in request.form:
            domestic = True
        else:
            domestic = False
        airline_ID = request.form['airline_ID']

        # Get the next flight_ID
        max_flight_ID = get_max_flight_ID()
        if max_flight_ID is None:
            return render_template(error_template, error="Unable to create flight. Please try again.")
        else: 
            flight_ID = str(max_flight_ID + 1)


        # Insert the flight
        insert_query = f"""
        INSERT INTO flight (flight_ID, port_of_origin, destination, departure_time, flight_length, domestic, airline_ID)
        VALUES ({flight_ID}, '{port_of_origin}', '{destination}', '{departure_time}', {flight_length}, {domestic}, {airline_ID})
        """

        execute_query(insert_query, error_template, error_message)

        return redirect(url_for("flight_directory.view", flight_ID=flight_ID))