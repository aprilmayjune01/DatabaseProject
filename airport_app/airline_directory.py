from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('airline_directory', __name__, template_folder='templates', url_prefix='/airline_directory')

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

@bp.route("/view/<airline_ID>")
def view(airline_ID):
    return redirect (url_for ('airline_directory.index'))

