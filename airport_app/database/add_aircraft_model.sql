ALTER TABLE aircraft 
ADD COLUMN model VARCHAR (50);

UPDATE aircraft
SET model = 'Boeing 737-800'
WHERE vessel_id = 1;

UPDATE aircraft
SET model = 'Boeing 737-800'
WHERE vessel_id = 2;

UPDATE aircraft
SET model = 'Airbus A320-200'
WHERE vessel_id = 3;

UPDATE aircraft
SET model = 'Airbus A320-200'
WHERE vessel_id = 4;

UPDATE aircraft
SET model = 'Airbus A320-200'
WHERE vessel_id = 5;

UPDATE aircraft
SET model = 'Airbus A400M'
WHERE vessel_id = 6;

UPDATE aircraft
SET model = 'Boeing 777-300ER'
WHERE vessel_id = 7;

UPDATE aircraft
SET model = 'Boeing 777-300ER'
WHERE vessel_id = 8;

UPDATE aircraft
SET model = 'Boeing 737 MAX 8'
WHERE vessel_id = 9;

UPDATE aircraft
SET model = 'Boeing 737 MAX 8'
WHERE vessel_id = 10;

UPDATE aircraft
SET model = 'Boeing 737 NG 800'
WHERE vessel_id = 11;

UPDATE aircraft
SET model = 'Airbus A350-900'
WHERE vessel_id = 12;

UPDATE aircraft
SET model = 'Airbus A220-300'
WHERE vessel_id = 13;

UPDATE aircraft
SET model = 'Airbus Beluga'
WHERE vessel_id = 14;

UPDATE aircraft
SET model = 'Airbus A380 Prestige'
WHERE vessel_id = 15;

ALTER TABLE aircraft
ALTER COLUMN model SET NOT NULL;