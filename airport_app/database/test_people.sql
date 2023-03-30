-- Aircraft staff
INSERT INTO people 
    (personal_ID, firstName, lastName, phone_no, email, home_address)
VALUES
    (100, 'John', 'Smith', 1234567890, 'test@test.com', '123 Test St');

INSERT INTO aircraft_staff 
    (personal_ID, employee_code, salary)
VALUES
    (100, '1234', 100000);


-- Pilot
INSERT INTO people 
    (personal_ID, firstName, lastName, phone_no, email, home_address)
VALUES
    (101, 'Jane', 'Doe', 1234567891, 'test2@test.com', '123 Test St');

INSERT INTO aircraft_staff 
    (personal_ID, employee_code, salary)
VALUES
    (101, '1235', 100000);

INSERT INTO pilot
    (personal_ID, eyesight, flight_hours)
VALUES
    (101, 2020, 1000);

INSERT INTO pilot_medical_conditions
    (pilot_id, medical_condition)
VALUES
    (101, 'asthma');

INSERT INTO certification
    (pilot_id, certification_type, date_of_issue)
VALUES
    (101, 'PPL', '2019-01-01');

