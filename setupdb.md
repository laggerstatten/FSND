psql

DROP DATABASE specimenfinder;


CREATE DATABASE specimenfinder;



psql -d specimenfinder

CREATE TABLE "Animal" (
    id SERIAL PRIMARY KEY,
    genus VARCHAR(120) NOT NULL,
    species VARCHAR(120) NOT NULL
);

CREATE TABLE "Institution" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    address VARCHAR(120) NOT NULL
);

CREATE TABLE "Specimen" (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER REFERENCES "Animal"(id) NOT NULL,
    institution_id INTEGER REFERENCES "Institution"(id) NOT NULL,
    sightingdate TIMESTAMP NOT NULL
);

INSERT INTO "Animal" (id, genus, species) VALUES
(1, 'Canis', 'lupus'),
(2, 'Felis', 'catus'),
(3, 'Panthera', 'leo');

INSERT INTO "Institution" (id, name, address) VALUES
(1, 'Zoo A', '123 Main St'),
(2, 'Wildlife Sanctuary B', '456 Oak Ave'),
(3, 'Research Institute C', '789 Elm Blvd');

INSERT INTO "Specimen" (id, animal_id, institution_id, sightingdate) VALUES
(1, 1, 1, '2023-01-15 10:30:00'),
(2, 2, 2, '2023-02-20 14:45:00'),
(3, 3, 3, '2023-03-10 09:00:00');
