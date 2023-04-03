from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('airline_directory', __name__, template_folder='templates', url_prefix='/airline_directory')



def get_airline(airline_ID): 
    """
    Returns a dictionary containing airline information.
    """

    select_query = f"""
    SELECT A.airline_ID, A.locations_based_in, A.phone_no, A.email, A.airline_name
    FROM airline A
    WHERE A.airline_ID = {airline_ID}
    """

    context = dict()

    try:
        cursor = g.conn.execute(text(select_query))
        for row in cursor:

            context['airline_ID'] = row[0]
            context['locations_based_in'] = row[1]
            context['phone_no'] = row[2]
            context['email'] = row[3]
            context['airline_name'] = row[4]
            break   # There should only be one row
        cursor.close()
        
    except Exception as e:
        print(e)
        return None

    select_query = f"""
    SELECT owns_aircraft.aircraft_ID, owns_aircraft.airline_ID, aircraft.model
    FROM owns_aircraft
    JOIN aircraft ON owns_aircraft.aircraft_ID = aircraft.vessel_ID
    WHERE owns_aircraft.airline_ID = {airline_ID}
    """

    try:
        cursor = g.conn.execute(text(select_query))
        owned_aircraft_models = []
        owned_aircraft_IDs = []

        for row in cursor:
            owned_aircraft_models.append(row[2])
            owned_aircraft_IDs.append(row[0])


            
        cursor.close()
        context[ 'owned_aircraft_models'] = owned_aircraft_models
        context[ 'owned_aircraft_IDs'] = owned_aircraft_IDs


    except Exception as e:
        print(e)

    
    return context

@bp.route("/")
def index():
    """
    Main page for airline_directory.
    Displays all the airlines.
    """

    select_query = """
    SELECT A.airline_ID, A.airline_name
    FROM airline A
    """

    airline_IDs = list()
    airline_names = list()
    context = dict()

    try:
        cursor = g.conn.execute(text(select_query))
        for result in cursor:
            airline_IDs.append(result[0])
            airline_names.append(result[1])
            
        cursor.close()

    except Exception as e:
        # log the error message or display a friendly error page to the user
        # here is an example of displaying the error message in the template
        print(e)

    context = {
            "airline_IDs": airline_IDs,
            "airline_names": airline_names,
            "num_airlines": len(airline_IDs)
        }

    return render_template("airline_directory.html", **context)

@bp.route("/view/<int:airline_ID>")
def view(airline_ID):
    context = get_airline(airline_ID)
    if context is None:
        return redirect(url_for('airline_directory.index'))
    
    return render_template('view_airline.html', **context)

@bp.route("/edit/<int:airline_ID>", methods=['GET', 'POST'])
def edit(airline_ID):
    context = get_airline(airline_ID)
    if context is None:
        return redirect(url_for('airline_directory.index'))

    if request.method == 'GET':
        return render_template('edit_airline.html', **context)
    
    if request.method == 'POST':
        
        locations_based_in= request.form['locations_based_in']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        airline_name = request.form['airline_name']

        update_airline_query = f"""
        UPDATE airline
        SET locations_based_in = '{locations_based_in}', phone_no = '{phone_no}', email = '{email}', airline_name = '{airline_name}'
        WHERE airline_ID = {airline_ID}
        """

        try:
            g.conn.execute(text(update_airline_query))
            g.conn.commit()
        except Exception as e:
            print(e)
            return render_template("edit_airline.html", error="Error: Could not update airline. Make sure all fields are filled out correctly.")
    return redirect(url_for("airline_directory.index"))

@bp.route("/delete/<int:airline_ID>")
def delete(airline_ID):
    delete_query = f"""
    DELETE FROM airline
    WHERE airline_ID = {airline_ID}
    """

    try:
        g.conn.execute(text(delete_query))
        g.conn.commit()
    except Exception as e:
        print(e)
        return redirect(url_for('airline_directory.index', error="Error: Could not delete airline."))
    return redirect(url_for("airline_directory.index"))

@bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create_airline.html')
    
    if request.method == 'POST':

        locations_based_in= request.form['locations_based_in']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        airline_name = request.form['airline_name']

        select_query = f"""
        SELECT MAX(airline_ID) 
        FROM airline
        """

        try:
            cursor = g.conn.execute(text(select_query))
            for result in cursor:
                airline_ID = result[0] + 1
                break   # There should only be one row
            cursor.close()
        except Exception as e:
            print(e)
            return render_template("create_airline.html", error="Error: Could not create airline. Please try again.")
        

        insert_airline_query = f"""
        INSERT INTO airline 
        VALUES ({airline_ID}, '{locations_based_in}', '{phone_no}', '{email}', '{airline_name}')
        """


        try:
            g.conn.execute(text(insert_airline_query))
            g.conn.commit()
        except Exception as e:
            print(e)
            return render_template("create_airline.html", error="Error: Could not create airline. Make sure all fields are filled out correctly.")


        return redirect(url_for('airline_directory.view', airline_ID=airline_ID))
   

