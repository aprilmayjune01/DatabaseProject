from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('staff_directory', __name__, template_folder='templates', url_prefix='/staff_directory')

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

def get_staff(personal_ID):
    """
    Returns a dictionary containing the staff member's information.
    """

    select_query = f"""
    SELECT P.firstName, P.lastName, P.phone_no, P.email, P.home_address, 
        A.employee_code, A.salary, PI.personal_ID
    FROM people P
    JOIN aircraft_staff A ON P.personal_ID = A.personal_ID
    LEFT JOIN pilot PI ON P.personal_ID = PI.personal_ID
    WHERE P.personal_ID = {personal_ID}
    """

    context = dict()

    try:
        cursor = g.conn.execute(text(select_query))
        for row in cursor:
            context['personal_ID'] = personal_ID
            context['first_name'] = row[0]
            context['last_name'] = row[1]
            context['phone_no'] = row[2]
            context['email'] = row[3]
            context['home_address'] = row[4]
            context['employee_code'] = row[5]
            context['salary'] = row[6]

            if row[7] is not None:  # If the staff member is a pilot
                context['is_pilot'] = True
            else:
                context['is_pilot'] = False
            break   # There should only be one row
        cursor.close()

    except Exception as e:
        print(e)
        return None

    return context

def get_pilot(personal_ID):
    """
    Returns a dictionary containing the pilot's information.
    """

    medical_conditions = list()
    certification_types = list()
    dates_of_issue = list()

    context = dict()
    context['personal_ID'] = personal_ID


    # Get pilot's basic information

    select_query = f"""
    SELECT P.eyesight, P.flight_hours
    FROM pilot P
    WHERE P.personal_ID = {personal_ID}
    """

    cursor = g.conn.execute(text(select_query))
    for row in cursor:
        context['eyesight'] = row[0]
        context['flight_hours'] = row[1]
        break   # There should only be one row
    cursor.close()


    # Get pilot's medical information

    select_query = f"""
    SELECT PMC.medical_condition
    FROM pilot_medical_conditions PMC 
    WHERE PMC.pilot_ID = {personal_ID}
    """

    cursor = g.conn.execute(text(select_query))
    for row in cursor:
        medical_conditions.append(row[0])
    cursor.close()


    # Get pilot's certification information
    select_query = f"""
    SELECT C.certification_type, C.date_of_issue
    FROM certification C
    WHERE C.pilot_ID = {personal_ID}
    """

    cursor = g.conn.execute(text(select_query))
    for row in cursor:
        certification_types.append(row[0])
        dates_of_issue.append(row[1])
    cursor.close()


    context['medical_conditions'] = medical_conditions
    context['certification_types'] = certification_types
    context['certification_dates_of_issue'] = dates_of_issue

    return context

### Routes ###

@bp.route("/")
def index():
    """
    Main page for staff_directory.
    Displays all staff members.
    """

    select_query = """
	SELECT P.personal_ID, P.firstName, P.lastName
	FROM people P, aircraft_staff A
	WHERE P.personal_ID = A.personal_ID
	"""

    personal_IDs = list()
    first_names = list()
    last_names = list()

    cursor = g.conn.execute(text(select_query))
    for result in cursor:
        personal_IDs.append(result[0])
        first_names.append(result[1])
        last_names.append(result[2])
    cursor.close()

    context = {
        "personal_IDs": personal_IDs,
        "first_names": first_names,
        "last_names": last_names,
        "num_entries": len(first_names)
    }

    return render_template("staff_directory.html", **context)

@bp.route("/view/<int:personal_ID>")
def view(personal_ID):
    context = get_staff(personal_ID)
    if context is None: # If the staff member does not exist
        return redirect(url_for('staff_directory.index'))

    if context['is_pilot']:   # Append pilot information if the staff member is a pilot
        pilot_context = get_pilot(personal_ID)
        context.update(pilot_context)

    return render_template("view_staff.html", **context)

@bp.route("/edit/<int:personal_ID>", methods=['GET', 'POST'])
def edit(personal_ID):
    context = get_staff(personal_ID)
    if context is None: # If the staff member does not exist
        return redirect(url_for('staff_directory.index'))
    
    if context['is_pilot']:   # Append pilot information if the staff member is a pilot
        pilot_context = get_pilot(personal_ID)
        context.update(pilot_context)
    
    if request.method == 'GET':
        return render_template("edit_staff.html", **context)
    
    if request.method == 'POST':
        error_message = 'Error: Failed to edit staff member - make sure to enter all fields correctly'    # Default error message
        error_render_template = 'edit_staff.html'    # Default error render template

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        home_address = request.form['home_address']
        employee_code = request.form['employee_code']
        salary = request.form['salary']
        if 'is_pilot' in request.form and request.form['is_pilot'] == 'on':
            is_pilot = True
            eyesight = request.form['eyesight']
            flight_hours = request.form['flight_hours']
            medical_conditions = request.form.getlist('medical_condition')
            certification_types = request.form.getlist('certification_type')
            certification_dates_of_issue = request.form.getlist('certification_date_of_issue')
        else: 
            is_pilot = False

        update_people_query = f"""
        UPDATE people
        SET firstName = '{first_name}', lastName = '{last_name}', phone_no = '{phone_no}', email = '{email}', home_address = '{home_address}'
        WHERE personal_ID = {personal_ID}
        """

        update_staff_query = f"""
        UPDATE aircraft_staff
        SET employee_code = '{employee_code}', salary = {salary}
        WHERE personal_ID = {personal_ID}
        """
        
        # All queries will be executed on the fly, to accommodate for sequential database insertions.
        execute_query(update_people_query, error_render_template, error_message)
        execute_query(update_staff_query, error_render_template, error_message)

        if is_pilot: 
            delete_pilot_query = f"""
            DELETE FROM pilot
            WHERE pilot_ID = {personal_ID}
            """

            execute_query(delete_pilot_query, error_render_template, error_message)

            insert_pilot_query = f""" 
            INSERT INTO pilot (pilot_ID, eyesight, flight_hours)
            VALUES ({personal_ID}, {eyesight}, {flight_hours})
            """

            execute_query(insert_pilot_query, error_render_template, error_message) 

            # Delete all pilot's medical conditions
            delete_pilot_medical_conditions_query = f"""
            DELETE FROM pilot_medical_conditions
            WHERE pilot_ID = {personal_ID}
            """

            execute_query(delete_pilot_medical_conditions_query, error_render_template, error_message)

            # Delete all pilot's certifications
            delete_certifications_query = f"""
            DELETE FROM certification
            WHERE pilot_ID = {personal_ID}
            """

            execute_query(delete_certifications_query, error_render_template, error_message)

            # Insert all pilot's medical conditions
            for medical_condition in medical_conditions:
                insert_pilot_medical_conditions_query = f"""
                INSERT INTO pilot_medical_conditions (pilot_ID, medical_condition)
                VALUES ({personal_ID}, '{medical_condition}')
                """

                execute_query(insert_pilot_medical_conditions_query, error_render_template, error_message)

            # Insert all pilot's certifications
            for i in range(len(certification_types)):
                insert_certifications_query = f"""
                INSERT INTO certification (pilot_ID, certification_type, date_of_issue)
                VALUES ({personal_ID}, '{certification_types[i]}', '{certification_dates_of_issue[i]}')
                """

                execute_query(insert_certifications_query, error_render_template, error_message)

        else:
            # Delete from pilot table if the staff member is no longer a pilot
            delete_pilot_query = f"""
            DELETE FROM pilot
            WHERE personal_ID = {personal_ID}
            """

            execute_query(delete_pilot_query, error_render_template, error_message)


        return redirect(url_for('staff_directory.view', personal_ID=personal_ID))

@bp.route("/delete/<int:personal_ID>")
def delete(personal_ID):
    delete_query = f"""
    DELETE FROM people
    WHERE personal_ID = {personal_ID}
    """

    execute_query(delete_query, 'staff_directory.index', 'Error: Could not delete staff member.')
    return redirect(url_for('staff_directory.index'))

@bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create_staff.html")
    
    if request.method == 'POST':
        error_message = 'Error: Failed to create staff member - make sure to enter all fields correctly'    # Default error message

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        home_address = request.form['home_address'] 
        employee_code = request.form['employee_code'] 
        salary = request.form['salary'] 
        if 'is_pilot' in request.form:
            is_pilot = True
            eyesight = request.form['eyesight']
            flight_hours = request.form['flight_hours']
            medical_conditions = request.form.getlist('medical_condition')
            certification_types = request.form.getlist('certification_type')
            dates_of_issue = request.form.getlist('certification_date_of_issue')
        else:
            is_pilot = False

        # Get the personal_ID of the new staff member

        select_query = """
        SELECT MAX(personal_ID)
        FROM people
        """

        cursor = g.conn.execute(text(select_query))
        for result in cursor:
            personal_ID = result[0] + 1
            break  # There should only be one row
        cursor.close()


        # Insert the new staff member into the database tables

        insert_people_query = f"""
        INSERT INTO people (personal_ID, firstName, lastName, phone_no, email, home_address)
        VALUES ('{personal_ID}', '{first_name}', '{last_name}', '{phone_no}', '{email}', '{home_address}')
        """

        insert_aircraft_staff_query = f"""
        INSERT INTO aircraft_staff (personal_ID, employee_code, salary)
        VALUES ({personal_ID}, '{employee_code}', {salary})
        """

        # All queries will be executed on the fly, to accommodate for sequential database insertions.
        execute_query(insert_people_query, 'create_staff.html', error_message)
        execute_query(insert_aircraft_staff_query, 'create_staff.html', error_message)

        if is_pilot:
            insert_pilot_query = f"""
            INSERT INTO pilot (personal_ID, eyesight, flight_hours)
            VALUES ({personal_ID}, '{eyesight}', {flight_hours})
            """

            execute_query(insert_pilot_query, 'create_staff.html', error_message)

            for i in range(len(medical_conditions)):
                insert_medical_condition_query = f"""
                INSERT INTO pilot_medical_conditions (pilot_ID, medical_condition)
                VALUES ({personal_ID}, '{medical_conditions[i]}')
                """
                
                # Query must be executed on the fly because the number of medical conditions is variable
                execute_query(insert_medical_condition_query, 'create_staff.html', error_message)
                
            
            for i in range(len(certification_types)):
                insert_certification_query = f"""
                INSERT INTO certification (pilot_ID, certification_type, date_of_issue)
                VALUES ({personal_ID}, '{certification_types[i]}', '{dates_of_issue[i]}')
                """

                # Query must be executed on the fly because the number of certifications is variable
                execute_query(insert_certification_query, 'create_staff.html', error_message)    

        return redirect(url_for('staff_directory.view', personal_ID=personal_ID))
    


#################### DEBUGGING FUNCTIONS ####################
@bp.route("/test")
def test_query():
    """
    Test function for development and debugging purposes. 
    Used to access the database.
    """

    personal_ID = 27

    select_query = f'''
    SELECT WF.flight_ID, F.destination, f.port_of_origin
    FROM works_flight WF
    JOIN flight F ON WF.flight_ID = F.flight_ID
    WHERE WF.staff_ID = {personal_ID}
    '''

    cursor = g.conn.execute(text(select_query))
    output = "Results: <br>"
    for result in cursor:
        output += str(result)
        output += "<br>"
    cursor.close()

    return output
