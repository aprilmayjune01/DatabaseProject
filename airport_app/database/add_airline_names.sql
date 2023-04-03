ALTER TABLE airline
ADD COLUMN airline_name VARCHAR(50);

UPDATE airline
SET airline_name = 'Air Canada'
WHERE airline_id = 1;

UPDATE airline
SET airline_name = 'WestJet'
WHERE airline_id = 2;

UPDATE airline
SET airline_name = 'Air Transat'
WHERE airline_id = 3;

UPDATE airline
SET airline_name = 'Air France'
WHERE airline_id = 4;

UPDATE airline
SET airline_name = 'Air India'
WHERE airline_id = 5;

UPDATE airline
SET airline_name = 'Air New Zealand'
WHERE airline_id = 6;

UPDATE airline
SET airline_name = 'Air China'
WHERE airline_id = 7;

UPDATE airline
SET airline_name = 'Air Berlin'
WHERE airline_id = 8;

UPDATE airline
SET airline_name = 'Air Malta'
WHERE airline_id = 9;

UPDATE airline
SET airline_name = 'Air Mauritius'
WHERE airline_id = 10;

UPDATE airline
SET airline_name = 'Air Serbia'
WHERE airline_id = 11;

UPDATE airline
SET airline_name = 'Air Tahiti Nui'
WHERE airline_id = 12;

UPDATE airline
SET airline_name = 'AirAsia'
WHERE airline_id = 13;

UPDATE airline
SET airline_name = 'Alaska Airlines'
WHERE airline_id = 14;

UPDATE airline
SET airline_name = 'Alitalia'
WHERE airline_id = 15;

ALTER TABLE airline 
ALTER COLUMN airline_name SET NOT NULL;