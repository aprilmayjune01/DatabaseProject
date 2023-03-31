from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('staff_directory', __name__, template_folder='templates', url_prefix='/staff_directory')

### Helper functions ###

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
    context['dates_of_issue'] = dates_of_issue

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
    if not context: # If the staff member does not exist
        return redirect(url_for('staff_directory.index'))

    if context['is_pilot']:   # Append pilot information if the staff member is a pilot
        pilot_context = get_pilot(personal_ID)
        context.update(pilot_context)
    return render_template("view_staff.html", **context)

@bp.route("/edit/<int:personal_ID>", methods=['GET', 'POST'])
def edit(personal_ID):
    context = get_staff(personal_ID)
    if not context: # If the staff member does not exist
        return redirect(url_for('staff_directory.index'))
    
    if request.method == 'GET':
        return render_template("edit_staff.html", **context)
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        home_address = request.form['home_address']
        employee_code = request.form['employee_code']
        salary = request.form['salary']

        update_people_query = f"""
        UPDATE people
        SET firstName = '{first_name}', lastName = '{last_name}', phone_no = {phone_no}, email = '{email}', home_address = '{home_address}'
        WHERE personal_ID = {personal_ID}
        """

        update_staff_query = f"""
        UPDATE aircraft_staff
        SET employee_code = '{employee_code}', salary = {salary}
        WHERE personal_ID = {personal_ID}
        """

        try:
            g.conn.execute(text(update_people_query))
            g.conn.execute(text(update_staff_query))
            g.conn.commit()
        except Exception as e:
            print(e)
            context['error'] = "Error: Invalid input. Make sure to enter all fields correctly."
            return render_template("edit_staff.html", **context)


        return redirect(url_for('staff_directory.view', personal_ID=personal_ID))

@bp.route("/delete/<int:personal_ID>")
def delete(personal_ID):
    delete_query = f"""
    DELETE FROM people
    WHERE personal_ID = {personal_ID}
    """

    g.conn.execute(text(delete_query))
    g.conn.commit()

    return redirect(url_for('staff_directory.index'))

@bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create_staff.html")
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        home_address = request.form['home_address'] 
        employee_code = request.form['employee_code'] 
        salary = request.form['salary'] 

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

        # TODO: Implement pilot-specific fields

        try:
            g.conn.execute(text(insert_people_query))
            g.conn.execute(text(insert_aircraft_staff_query))
            g.conn.commit()
        except Exception as exception:
            print(exception)
            return render_template("create_staff.html", error="Failed to create staff member - make sure to enter all fields correctly")


        return redirect(url_for('staff_directory.index'))
    


#################### DEBUGGING FUNCTIONS ####################
def test_query():
    """
    Test function for development and debugging purposes. 
    Used to access the database.
    """


    select_query = """
    SELECT *
    FROM people
    LEFT JOIN aircraft_staff ON people.personal_ID = aircraft_staff.personal_ID
    LEFT JOIN pilot ON people.personal_ID = pilot.personal_ID
    WHERE people.personal_ID = 31
    """

    cursor = g.conn.execute(text(select_query))
    print('Results:')
    for result in cursor:
        print(result)
    cursor.close()
