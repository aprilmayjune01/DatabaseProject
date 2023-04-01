from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('passenger_directory', __name__, template_folder='templates', url_prefix='/passenger_directory')

### Helper functions ###

def get_passenger(personal_ID): 
    """
    Returns a dictionary containing the passenger's information.
    """

    select_query = f"""
    SELECT P.firstName, P.lastName, P.phone_no, P.email, P.home_address, 
        PG.passport_no
    FROM people P
    JOIN passenger PG ON P.personal_ID = PG.personal_ID
    WHERE P.personal_ID = {personal_ID}
    """

    context = dict()

    cursor = g.conn.execute(text(select_query))
    for row in cursor:
        context['personal_ID'] = personal_ID
        context['first_name'] = row[0]
        context['last_name'] = row[1]
        context['phone_no'] = row[2]
        print(f'In cursor: {row[2]}')
        context['email'] = row[3]
        context['home_address'] = row[4]
        context['passport_no'] = row[5]
        break   # There should only be one row
    cursor.close()

    print(f'In context: {context["phone_no"]}')

    return context


### Routes ###

@bp.route('/')
def index():
    """
    Main page for the passenger directory.
    Displays all passengers.
    """

    select_query = """
    SELECT P.personal_ID, P.firstName, P.lastName
    FROM people P, passenger PG
    WHERE P.personal_ID = PG.personal_ID
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

    return render_template('passenger_directory.html', **context)

@bp.route('/view/<int:personal_ID>')
def view(personal_ID):
    context = get_passenger(personal_ID)
    if not context:
        return redirect(url_for('passenger_directory.index'))
    
    return render_template('view_passenger.html', **context)

@bp.route('/edit/<int:personal_ID>', methods=['GET', 'POST'])
def edit(personal_ID):
    context = get_passenger(personal_ID)
    if not context:
        return redirect(url_for('passenger_directory.index'))

    if request.method == 'GET':
        return render_template('edit_passenger.html', **context)
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        home_address = request.form['home_address']
        passport_no = request.form['passport_no']

        update_people_query = f"""
        UPDATE people
        SET firstName = '{first_name}', lastName = '{last_name}', phone_no = '{phone_no}', email = '{email}', home_address = '{home_address}'
        WHERE personal_ID = {personal_ID}
        """

        update_passenger_query = f"""
        UPDATE passenger
        SET passport_no = '{passport_no}'
        WHERE personal_ID = {personal_ID}
        """

        try:
            g.conn.execute(text(update_people_query))
            g.conn.execute(text(update_passenger_query))
            g.conn.commit()
        except Exception as e:
            print(e)
            return render_template("edit_passenger.html", error="Error: Could not update passenger. Make sure all fields are filled out correctly.")

        return redirect(url_for('passenger_directory.view',  personal_ID=personal_ID))

@bp.route('/delete/<int:personal_ID>')
def delete(personal_ID):
    delete_query = f"""
    DELETE FROM people
    WHERE personal_ID = {personal_ID}
    """

    try:
        g.conn.execute(text(delete_query))
        g.conn.commit()
    except Exception as e:
        print(e)
        return redirect(url_for('passenger_directory.index', error="Error: Could not delete passenger."))
        
    return redirect(url_for('passenger_directory.index'))
    

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create_passenger.html')
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email'] 
        home_address = request.form['home_address']
        passport_no = request.form['passport_no']

        select_query = f"""
        SELECT MAX(personal_ID) 
        FROM people
        """

        cursor = g.conn.execute(text(select_query))
        for result in cursor:
            personal_ID = result[0] + 1
            break   # There should only be one row
        cursor.close()

        insert_people_query = f"""
        INSERT INTO people 
        VALUES ({personal_ID}, '{first_name}', '{last_name}', '{phone_no}', '{email}', '{home_address}')
        """

        insert_passenger_query = f"""
        INSERT INTO passenger
        VALUES ({personal_ID}, '{passport_no}')
        """

        try:
            g.conn.execute(text(insert_people_query))
            g.conn.execute(text(insert_passenger_query))
            g.conn.commit()
        except Exception as e:
            print(e)
            return render_template("create_passenger.html", error="Error: Could not create passenger. Make sure all fields are filled out correctly.")


        return redirect(url_for('passenger_directory.view', personal_ID=personal_ID))


