ALTER TABLE cargo_aircraft
DROP CONSTRAINT cargo_aircraft_vessel_id_fkey,
ADD CONSTRAINT cargo_aircraft_vessel_id_fkey
    FOREIGN KEY (vessel_id) 
    REFERENCES aircraft(vessel_id)
    ON DELETE CASCADE;

ALTER TABLE passenger_aircraft
DROP CONSTRAINT passenger_aircraft_vessel_id_fkey,
ADD CONSTRAINT passenger_aircraft_vessel_id_fkey
    FOREIGN KEY (vessel_id) 
    REFERENCES aircraft(vessel_id)
    ON DELETE CASCADE;

ALTER TABLE flight 
DROP CONSTRAINT flight_airline_id_fkey,
ADD CONSTRAINT flight_airline_id_fkey
    FOREIGN KEY (airline_id) 
    REFERENCES airline(airline_id)
    ON DELETE CASCADE;

ALTER TABLE passenger 
DROP CONSTRAINT passenger_personal_id_fkey,
ADD CONSTRAINT passenger_personal_id_fkey
    FOREIGN KEY (personal_id) 
    REFERENCES people(personal_id)
    ON DELETE CASCADE;

ALTER TABLE aircraft_staff 
DROP CONSTRAINT aircraft_staff_personal_id_fkey,
ADD CONSTRAINT aircraft_staff_personal_id_fkey
    FOREIGN KEY (personal_id) 
    REFERENCES people(personal_id)
    ON DELETE CASCADE;

ALTER TABLE pilot
DROP CONSTRAINT pilot_personal_id_fkey,
ADD CONSTRAINT pilot_personal_id_fkey
    FOREIGN KEY (personal_id) 
    REFERENCES aircraft_staff(personal_id)
    ON DELETE CASCADE;

ALTER TABLE pilot_medical_conditions 
DROP CONSTRAINT pilot_medical_conditions_pilot_id_fkey,
ADD CONSTRAINT pilot_medical_conditions_pilot_id_fkey
    FOREIGN KEY (pilot_id) 
    REFERENCES pilot(personal_id)
    ON DELETE CASCADE;

ALTER TABLE certification 
DROP CONSTRAINT certification_pilot_id_fkey,
ADD CONSTRAINT certification_pilot_id_fkey
    FOREIGN KEY (pilot_id) 
    REFERENCES pilot(personal_id)
    ON DELETE CASCADE;

ALTER TABLE booking
DROP CONSTRAINT booking_passenger_id_fkey,
ADD CONSTRAINT booking_passenger_id_fkey
    FOREIGN KEY (passenger_id) 
    REFERENCES passenger(personal_id)
    ON DELETE CASCADE;

ALTER TABLE booking_seats
DROP CONSTRAINT booking_seats_reference_no_fkey,
ADD CONSTRAINT booking_seats_reference_no_fkey
    FOREIGN KEY (reference_no) 
    REFERENCES booking(reference_no)
    ON DELETE CASCADE;

ALTER TABLE owns_aircraft
DROP CONSTRAINT owns_aircraft_aircraft_id_fkey,
ADD CONSTRAINT owns_aircraft_aircraft_id_fkey
    FOREIGN KEY (aircraft_id) 
    REFERENCES aircraft(vessel_id)
    ON DELETE CASCADE;

ALTER TABLE owns_aircraft
DROP CONSTRAINT owns_aircraft_airline_id_fkey,
ADD CONSTRAINT owns_aircraft_airline_id_fkey
    FOREIGN KEY (airline_id) 
    REFERENCES airline(airline_id)
    ON DELETE CASCADE;

ALTER TABLE works_flight
DROP CONSTRAINT works_flight_staff_id_fkey,
ADD CONSTRAINT works_flight_staff_id_fkey
    FOREIGN KEY (staff_id) 
    REFERENCES aircraft_staff(personal_id)
    ON DELETE CASCADE;

ALTER TABLE works_flight
DROP CONSTRAINT works_flight_flight_id_fkey,
ADD CONSTRAINT works_flight_flight_id_fkey
    FOREIGN KEY (flight_id) 
    REFERENCES flight(flight_id)
    ON DELETE CASCADE;

ALTER TABLE flies 
DROP CONSTRAINT flies_pilot_id_fkey,
ADD CONSTRAINT flies_pilot_id_fkey
    FOREIGN KEY (pilot_id) 
    REFERENCES pilot(personal_id)
    ON DELETE CASCADE;

ALTER TABLE flies
DROP CONSTRAINT flies_flight_id_fkey,
ADD CONSTRAINT flies_flight_id_fkey
    FOREIGN KEY (flight_id) 
    REFERENCES flight(flight_id)
    ON DELETE CASCADE;

ALTER TABLE employs 
DROP CONSTRAINT employs_airline_id_fkey,
ADD CONSTRAINT employs_airline_id_fkey
    FOREIGN KEY (airline_id) 
    REFERENCES airline(airline_id)
    ON DELETE CASCADE;

ALTER TABLE employs
DROP CONSTRAINT employs_staff_id_fkey,
ADD CONSTRAINT employs_staff_id_fkey
    FOREIGN KEY (staff_id) 
    REFERENCES aircraft_staff(personal_id)
    ON DELETE CASCADE;

ALTER TABLE flown_with_vessel
DROP CONSTRAINT flown_with_vessel_aircraft_id_fkey,
ADD CONSTRAINT flown_with_vessel_aircraft_id_fkey
    FOREIGN KEY (aircraft_id) 
    REFERENCES aircraft(vessel_id)
    ON DELETE CASCADE;

ALTER TABLE flown_with_vessel
DROP CONSTRAINT flown_with_vessel_flight_id_fkey,
ADD CONSTRAINT flown_with_vessel_flight_id_fkey
    FOREIGN KEY (flight_id) 
    REFERENCES flight(flight_id)
    ON DELETE CASCADE;

ALTER TABLE booked_flights
DROP CONSTRAINT booked_flights_flight_id_fkey,
ADD CONSTRAINT booked_flights_flight_id_fkey
    FOREIGN KEY (flight_id) 
    REFERENCES flight(flight_id)
    ON DELETE CASCADE;

ALTER TABLE booked_flights
DROP CONSTRAINT booked_flights_reference_no_fkey,
ADD CONSTRAINT booked_flights_reference_no_fkey
    FOREIGN KEY (reference_no) 
    REFERENCES booking(reference_no)
    ON DELETE CASCADE;

