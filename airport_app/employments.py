from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('employments', __name__, template_folder='templates' , url_prefix='/employments')

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

def get_employment_data(personal_ID):
    """ Get employment data for a given aircraft staff member """
    
    # Check if the personal ID belongs to aircraft staff

    check_is_aircraft_staff_query = f"""
    SELECT personal_ID
    FROM aircraft_staff
    WHERE personal_ID = {personal_ID}
    """

    cursor = g.conn.execute(text(check_is_aircraft_staff_query))
    result = cursor.fetchone()
    cursor.close()

    if result is None:  # If personal ID doesn't belong to aircraft staff, return None
        return None
    
    
    # If person is aircraft staff member, get employment data

    context = dict()

    # Get staff member name

    select_name_query = f"""
    SELECT firstName, lastName
    FROM people
    WHERE personal_ID = {personal_ID}
    """

    try: 
        cursor = g.conn.execute(text(select_name_query))
        result = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print(e)
        return None     # If can't get name, return None - something is wrong.


    employer_IDs = list()
    employer_names = list()
    flights_worked_IDs = list()
    flights_worked_destinations = list()
    flights_worked_origins = list()

    select_employment_query = f''' 
    SELECT E.airline_ID, A.airline_name
    FROM employs E
    JOIN airline A ON E.airline_ID = A.airline_ID
    WHERE E.staff_ID = {personal_ID}
    '''

    try:
        cursor = g.conn.execute(text(select_employment_query))
        for result in cursor:
            employer_IDs.append(result[0])
            employer_names.append(result[1])
        cursor.close()
    except Exception as e:
        print(e)

    context['employer_IDs'] = employer_IDs    # List of airline (employer) IDs
    context['employer_names'] = employer_names    # List of airline (employer) names

    # Get flights worked 

    select_flights_worked_query = f'''
    SELECT WF.flight_ID, F.destination, f.port_of_origin
    FROM works_flight WF
    JOIN flight F ON WF.flight_ID = F.flight_ID
    WHERE WF.staff_ID = {personal_ID}
    '''

    try:
        cursor = g.conn.execute(text(select_flights_worked_query))
        for result in cursor:
            flights_worked_IDs.append(result[0])
            flights_worked_destinations.append(result[1])
            flights_worked_origins.append(result[2])
        cursor.close()
    except Exception as e:
        print(e)

    context['flights_worked_IDs'] = flights_worked_IDs
    context['flights_worked_destinations'] = flights_worked_destinations
    context['flights_worked_origins'] = flights_worked_origins


    # Check if the personal ID belongs to a pilot

    check_is_pilot_query = f"""
    SELECT P.personal_ID
    FROM aircraft_staff A
    LEFT JOIN pilot P ON A.personal_ID = P.personal_ID
    WHERE A.personal_ID = {personal_ID}
    """

    try:
        cursor = g.conn.execute(text(check_is_pilot_query))
        result = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print(e)
        result[0] = None

    if result[0] is None:
        is_pilot = False
    else:
        is_pilot = True

    context['is_pilot'] = is_pilot

    # Get data for flights piloted

    if is_pilot:
        flights_piloted_IDs = list()
        flights_piloted_destinations = list()
        flights_piloted_origins = list()

        select_flights_piloted_query = f'''
        SELECT F.flight_ID, F.destination, F.port_of_origin
        FROM flies FL
        JOIN flight F ON FL.flight_ID = F.flight_ID
        WHERE FL.pilot_ID = {personal_ID}
        '''

        try:
            cursor = g.conn.execute(text(select_flights_piloted_query))
            for result in cursor:
                flights_piloted_IDs.append(result[0])
                flights_piloted_destinations.append(result[1])
                flights_piloted_origins.append(result[2])
            cursor.close()
        except Exception as e:
            print(e)

        context['flights_piloted_IDs'] = flights_piloted_IDs
        context['flights_piloted_destinations'] = flights_piloted_destinations
        context['flights_piloted_origins'] = flights_piloted_origins

    return context




### Routes ###

@bp.route('/')
def index():
    """ Main page for employments """

    context = dict()

    select_query = f'''
    SELECT P.personal_ID, P.firstName, P.lastName
    FROM people P, aircraft_staff A
    WHERE P.personal_ID = A.personal_ID
    '''

    personal_IDs = list()
    first_names = list()
    last_names = list()

    cursor = g.conn.execute(text(select_query))
    for result in cursor:
        personal_IDs.append(result[0])
        first_names.append(result[1])
        last_names.append(result[2])
    cursor.close()

    context['personal_IDs'] = personal_IDs
    context['first_names'] = first_names
    context['last_names'] = last_names

    return render_template('employments.html', **context)   

@bp.route('/view/<personal_ID>')
def view(personal_ID):
    """ View employment details for an aircraft staff member """

    context = get_employment_data(personal_ID)

    if context is None:
        return redirect(url_for('employments.index'))

    return render_template('view_employments.html', **context)

@bp.route('/manage/<personal_ID>', methods=['GET', 'POST'])
def manage(personal_ID):
    """ Edit employment details for an aircraft staff member """

    context = get_employment_data(personal_ID)

    if context is None:
        return redirect(url_for('employments.index'))
    
    if request.method == 'GET':
        return render_template('edit_employment.html', **context)
    
    if request.method == 'POST':
        return redirect(url_for('employments.index'))
    



