from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('aircraft_directory', __name__, template_folder='templates', url_prefix='/aircraft_directory')

### Helper functions ###

def get_aircraft(vessel_ID):
    """
    Returns a dictionary containing the aircraft's information.
    """

    select_aircraft_query = f"""
    SELECT A.vessel_ID, A.fuel_capacity, A.domestic, A.model
    FROM aircraft A
    WHERE A.vessel_ID = {vessel_ID}
    """

    select_cargo_query = f"""
    SELECT C.weight_limit 
    FROM cargo_aircraft C, aircraft A
    WHERE C.vessel_ID = A.vessel_ID AND A.vessel_ID = {vessel_ID}
    """

    select_passenger_query = f"""
    SELECT P.passenger_capacity, P.is_private
    FROM passenger_aircraft P, aircraft A
    WHERE P.vessel_ID = A.vessel_ID AND A.vessel_ID = {vessel_ID}
    """

    context = dict()

    try:
        cursor = g.conn.execute(text(select_aircraft_query))
        for row in cursor:
            context['vessel_ID'] = row[0]
            context['fuel_capacity'] = row[1]
            context['domestic'] = row[2]
            context['model'] = row[3]
            break   # There should only be one row
        cursor.close()

        cursor = g.conn.execute(text(select_cargo_query))
        for row in cursor:
            context['weight_limit'] = row[0]
            context['aircraft_type'] = 'cargo'
            break  # There should only be one row
        cursor.close()

        cursor = g.conn.execute(text(select_passenger_query))
        for row in cursor:
            context['passenger_capacity'] = row[0]
            context['is_private'] = row[1]
            context['aircraft_type'] = 'passenger'
            break   # There should only be one row
        cursor.close()

    except Exception as e:
        print(e)
        return None

    return context


### Routes ###

@bp.route('/')
def index():
    """
    Main page for the aircraft directory.
    Displays all aircraft.
    """

    select_query = """
    SELECT A.vessel_ID, A.model
    FROM aircraft A
    """

    vessel_IDs = list()
    models = list()

    try:
        cursor = g.conn.execute(text(select_query))
        for row in cursor:
            vessel_IDs.append(row[0])
            models.append(row[1])
        cursor.close()

    except Exception as e:
        print(e)

    context = dict(
        vessel_IDs=vessel_IDs,
        models=models,
        num_vessels=len(vessel_IDs)
    )

    return render_template('aircraft_directory.html', **context)

@bp.route('/view/<vessel_ID>')
def view(vessel_ID):
    """
    View details for a specific aircraft.
    """

    context = get_aircraft(vessel_ID)
    if context is None or not context:
        return redirect(url_for('aircraft_directory.index'))    

    return render_template('view_aircraft.html', **context)

@bp.route('/edit/<vessel_ID>', methods=['GET', 'POST'])
def edit(vessel_ID):
    """
    Edit details for a specific aircraft.
    """

    context = get_aircraft(vessel_ID)
    if context is None:
        return redirect(url_for('aircraft_directory.index'))

    if request.method == 'GET':
        return render_template('edit_aircraft.html', **context)

    if request.method == 'POST':
        model = request.form['model']
        fuel_capacity = request.form['fuel_capacity']
        if 'domestic' in request.form:
            domestic = True
        else:
            domestic = False

        # Update the database
        update_query = f"""
        UPDATE aircraft
        SET model = '{model}',
            fuel_capacity = {fuel_capacity},
            domestic = {domestic}
        WHERE vessel_ID = {vessel_ID}
        """

        # Cargo-specific fields
        if request.form['aircraft_type'] == 'cargo':
            weight_limit = request.form['weight_limit']

            update_cargo_query = f"""
            UPDATE cargo_aircraft
            SET weight_limit = {weight_limit}
            WHERE vessel_ID = {vessel_ID}
            """

        elif request.form['aircraft_type'] == 'passenger':
            passenger_capacity = request.form['passenger_capacity']
            if 'is_private' in request.form:
                is_private = True
            else:
                is_private = False

            update_passenger_query = f"""
            UPDATE passenger_aircraft
            SET passenger_capacity = {passenger_capacity},
                is_private = {is_private}
            WHERE vessel_ID = {vessel_ID}
            """

        try:
            g.conn.execute(text(update_query))
            if request.form['aircraft_type'] == 'cargo':
                g.conn.execute(text(update_cargo_query))
            elif request.form['aircraft_type'] == 'passenger':
                g.conn.execute(text(update_passenger_query))
            g.conn.commit()
        except Exception as e:
            print(e)
            return render_template('edit_aircraft.html', error='Error updating aircraft. Make sure all fields are filled out correctly.')

        return redirect(url_for('aircraft_directory.view', vessel_ID=vessel_ID))
    
@bp.route('/delete/<vessel_ID>')
def delete(vessel_ID):
    """
    Delete an aircraft.
    """

    delete_query = f"""
    DELETE FROM aircraft
    WHERE vessel_ID = {vessel_ID}
    """

    try:
        g.conn.execute(text(delete_query))
        g.conn.commit()
    except Exception as e:
        print(e)

    return redirect(url_for('aircraft_directory.index'))

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """
    Create a new aircraft.
    """

    if request.method == 'GET':
        return render_template('create_aircraft.html')
    
    if request.method == 'POST':
        model = request.form['model']
        fuel_capacity = request.form['fuel_capacity']
        if 'domestic' in request.form:
            domestic = True
        else:
            domestic = False

        # Get new vessel_ID
        select_query = """
        SELECT MAX(vessel_ID) 
        FROM aircraft
        """

        try:
            cursor = g.conn.execute(text(select_query))
            for row in cursor:
                vessel_ID = row[0] + 1
                break
            cursor.close()
        except Exception as e:
            print(e)
            return render_template('create_aircraft.html', error='Error creating aircraft. Please try again.')
        
        # Insert into aircraft
        insert_aircraft_query = f"""
        INSERT INTO aircraft (vessel_ID, model, fuel_capacity, domestic)
        VALUES ({vessel_ID}, '{model}', {fuel_capacity}, {domestic})
        """

        # Insert into cargo
        if request.form['aircraft_type'] == 'cargo':
            weight_limit = request.form['weight_limit']

            insert_cargo_query = f"""
            INSERT INTO cargo_aircraft (vessel_ID, weight_limit)
            VALUES ({vessel_ID}, {weight_limit})
            """

            try:
                g.conn.execute(text(insert_aircraft_query))
                g.conn.execute(text(insert_cargo_query))
                g.conn.commit()
            except Exception as e:
                print(e)
                return render_template('create_aircraft.html', error='Error creating aircraft. Please try again.')
            
        # Insert into passenger 
        elif request.form['aircraft_type'] == 'passenger':
            passenger_capacity = request.form['passenger_capacity']
            if 'is_private' in request.form:
                is_private = True
            else:
                is_private = False

            insert_passenger_query = f"""
            INSERT INTO passenger_aircraft (vessel_ID, passenger_capacity, is_private)
            VALUES ({vessel_ID}, {passenger_capacity}, {is_private})
            """

            try:
                g.conn.execute(text(insert_aircraft_query))
                g.conn.execute(text(insert_passenger_query))
                g.conn.commit()
            except Exception as e:
                print(e)
                return render_template('create_aircraft.html', error='Error creating aircraft. Please try again.')

        return redirect(url_for('aircraft_directory.view', vessel_ID=vessel_ID))

    