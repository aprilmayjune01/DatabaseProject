DROP TABLE IF EXISTS airline;
CREATE TABLE airline (
    airline_id VARCHAR (10) PRIMARY KEY,
    locations_based_in VARCHAR (200) NOT NULL,
    phone_no VARCHAR (50) NOT NULL,
    email VARCHAR (50) NOT NULL
);

DROP TABLE IF EXISTS aircraft;
CREATE TABLE aircraft (
    vessel_id INT PRIMARY KEY,
    fuel_capacity NUMERIC NOT NULL CHECK (fuel_capacity > 0),
    domestic BOOLEAN NOT NULL
);

DROP TABLE IF EXISTS cargo_aircraft;
CREATE TABLE cargo_aircraft (
    vessel_id INT NOT NULL,
    weight_limit NUMERIC NOT NULL CHECK (weight_limit > 0),
    FOREIGN KEY (vessel_id) REFERENCES aircraft(vessel_id),
    PRIMARY KEY (vessel_id)
);

DROP TABLE IF EXISTS passenger_aircraft;
CREATE TABLE passenger_aircraft (
    vessel_id INT NOT NULL,
    passenger_capacity INT NOT NULL CHECK (passenger_capacity > 0),
    is_private BOOLEAN NOT NULL,
    FOREIGN KEY (vessel_id) REFERENCES aircraft(vessel_id),
    PRIMARY KEY (vessel_id)
);

DROP TABLE IF EXISTS flight;
CREATE TABLE flight (
    flight_ID VARCHAR (50) PRIMARY KEY,
    destination VARCHAR (100) NOT NULL,
    port_of_origin VARCHAR (100) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    flight_length NUMERIC NOT NULL CHECK (flight_length > 0),
    domestic BOOLEAN NOT NULL,
    airline_id INT NOT NULL,
    FOREIGN KEY (airline_id) REFERENCES airline(airline_id)
);


DROP TABLE IF EXISTS people;
CREATE TABLE people (
    personal_ID INT PRIMARY KEY,
    firstName VARCHAR (50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    phone_no INT NOT NULL,
    email VARCHAR (50) NOT NULL,
    home_address VARCHAR (100) NOT NULL
);

DROP TABLE IF EXISTS passenger;
CREATE TABLE passenger (
    personal_ID INT NOT NULL,
    passport_no INT NOT NULL,
    FOREIGN KEY (personal_ID) REFERENCES people (personal_ID),
    PRIMARY KEY (personal_ID)
);

DROP TABLE IF EXISTS aircraft_staff;
CREATE TABLE aircraft_staff(
    personal_ID INT NOT NULL,
    employee_code VARCHAR(50) NOT NULL,
    salary INT NOT NULL CHECK (salary > 0),
    FOREIGN KEY (personal_ID) REFERENCES people (personal_ID),
    PRIMARY KEY (personal_ID)
);

DROP TABLE IF EXISTS pilot;
CREATE TABLE pilot(
    personal_ID INT NOT NULL, 
    eyesight VARCHAR(50) NOT NULL,
    flight_hours INT NOT NULL,
    FOREIGN KEY (personal_ID) REFERENCES aircraft_staff(personal_ID),
    PRIMARY KEY (personal_ID)
);

DROP TABLE IF EXISTS pilot_medical_conditions;
CREATE TABLE pilot_medical_conditions(
    pilot_id INT NOT NULL,
    medical_condition VARCHAR(50) NOT NULL,
    FOREIGN KEY (pilot_id) REFERENCES pilot(personal_ID),
    PRIMARY KEY (pilot_id, medical_condition)
);

DROP TABLE IF EXISTS certification;
CREATE TABLE certification (
    pilot_id INT NOT NULL,
    certification_type VARCHAR(50) NOT NULL,
    date_of_issue DATE NOT NULL,
    FOREIGN KEY (pilot_id) REFERENCES pilot(personal_ID),
    PRIMARY KEY (pilot_id, certification_type)
);

DROP TABLE IF EXISTS booking;
CREATE TABLE booking (
    reference_no INT PRIMARY KEY,
    cost NUMERIC NOT NULL CHECK (cost >= 0),
    baggage_allowance INT NOT NULL CHECK (baggage_allowance >= 0),
    passenger_id INT NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES passenger(personal_ID)
);

DROP TABLE IF EXISTS booking_seats;
CREATE TABLE booking_seats (
    reference_no INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    FOREIGN KEY (reference_no) REFERENCES booking(reference_no),
    PRIMARY KEY (reference_no, seat_number)
);

DROP TABLE IF EXISTS owns_aircraft;
CREATE TABLE owns_aircraft (
    aircraft_id INT UNIQUE NOT NULL,
    airline_id INT NOT NULL,
    FOREIGN KEY (aircraft_id) REFERENCES aircraft(vessel_id),
    FOREIGN KEY (airline_id) REFERENCES airline(airline_id),
    PRIMARY KEY (aircraft_id, airline_id)
);

DROP TABLE IF EXISTS works_flight;
CREATE TABLE works_flight (
    staff_id INT NOT NULL,
    flight_id VARCHAR (50) NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES aircraft_staff(personal_id),
    FOREIGN KEY (flight_id) REFERENCES flight(flight_id),
    PRIMARY KEY (staff_id, flight_id)
);

DROP TABLE IF EXISTS flies;
CREATE TABLE flies (
    pilot_id INT NOT NULL,
    flight_id VARCHAR (50) NOT NULL,
    FOREIGN KEY (pilot_id) REFERENCES pilot(personal_id),
    FOREIGN KEY (flight_id) REFERENCES flight(flight_id),
    PRIMARY KEY (pilot_id, flight_id)
);

DROP TABLE IF EXISTS employs;
CREATE TABLE employs (
    airline_id INT NOT NULL,
    staff_id INT NOT NULL,
    FOREIGN KEY (airline_id) REFERENCES airline(airline_id),
    FOREIGN KEY (staff_id) REFERENCES aircraft_staff(personal_id),
    PRIMARY KEY (airline_id, staff_id)
);

DROP TABLE IF EXISTS flown_with_vessel;
CREATE TABLE flown_with_vessel (
    aircraft_id INT NOT NULL,
    flight_id VARCHAR (50) UNIQUE NOT NULL,
    FOREIGN KEY (aircraft_id) REFERENCES aircraft(vessel_id),
    FOREIGN KEY (flight_id) REFERENCES flight(flight_id),
    PRIMARY KEY (aircraft_id, flight_id)
);

DROP TABLE IF EXISTS booked_flights;
CREATE TABLE booked_flights (
    reference_no INT NOT NULL,
    flight_id VARCHAR (50) NOT NULL,
    FOREIGN KEY (reference_no) REFERENCES booking(reference_no),
    FOREIGN KEY (flight_id) REFERENCES flight(flight_id),
    PRIMARY KEY (reference_no, flight_id)
);





