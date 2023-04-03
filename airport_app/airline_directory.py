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
    SELECT * FROM airline 
    """

    airline_ids = list()
    locations_based_ins = list()
    phone_nos = list()
    emails = list()

    try:
        cursor = g.conn.execute(text(select_query))
        for result in cursor:
            airline_ids.append(result[0])
            locations_based_ins.append(result[1])
            phone_nos.append(result[2])
            emails.append(result[3])
        cursor.close()

        context = {
            "airline_ids": airline_ids,
            "locations_based_ins": locations_based_ins,
            "phone_nos": phone_nos,
            "emails": emails,
        }

        return render_template("airline_directory.html", **context)

    except Exception as e:
        # log the error message or display a friendly error page to the user
        # here is an example of displaying the error message in the template
        context = {
            "error_message": str(e)
        }
        return render_template("error.html", **context)
