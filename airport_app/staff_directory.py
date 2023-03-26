from flask import Flask, render_template, redirect, url_for, Blueprint, g, request
from sqlalchemy import text

bp = Blueprint('staff_directory', __name__, template_folder='templates', url_prefix='/staff_directory')

@bp.route("/")
def index():
    """
    Main page for staff_directory.
    Displays all staff members.
    """

    select_query = """
	SELECT P.firstName, P.lastName, P.phone_no, P.email, P.home_address, A.employee_code, A.salary
	FROM people P, aircraft_staff A
	WHERE P.personal_ID = A.personal_ID
	"""

    first_names = list()
    last_names = list()
    phone_nos = list()
    emails = list()
    home_addresses = list()
    employee_codes = list()
    salaries = list()


    cursor = g.conn.execute(text(select_query))
    for result in cursor:
        first_names.append(result[0])
        last_names.append(result[1])
        phone_nos.append(result[2])
        emails.append(result[3])
        home_addresses.append(result[4])
        employee_codes.append(result[5])
        salaries.append(result[6])
    cursor.close()

    context = {
        "first_names": first_names,
        "last_names": last_names,
        "phone_nos": phone_nos,
        "emails": emails,
        "home_addresses": home_addresses,
        "employee_codes": employee_codes,
        "salaries": salaries,
        "num_entries": len(first_names)
    }

    return render_template("staff_directory.html", **context)