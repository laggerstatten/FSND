
"C:\Program Files\PostgreSQL\14\data\pg_hba.conf"



/c/Users/darwi/AppData/Local/Programs/Python/Python37/python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
FLASK_APP=app.py FLASK_DEBUG=true flask run








Gitbash::::

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

psql


psql::::

CREATE DATABASE fyyur_db;


Gitbash::::

source venv/Scripts/activate
FLASK_APP=app.py FLASK_DEBUG=true flask run


Gitbash::::

source venv/Scripts/activate
flask db init

psql::::
\c fyyur_db
\dt

INSERT INTO "Venue" (id, name,  address, city, state, phone, facebook_link, image_link)
VALUES (
    1, 
    'The Musical Hop', 
    '1015 Folsom Street', 
    'San Francisco', 
    'CA', 
    '123-123-1234', 
    'https://www.facebook.com/TheMusicalHop', 
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
);

INSERT INTO "Venue" (id, name,  address, city, state, phone, facebook_link,  image_link)
VALUES (
    2, 
    'The Dueling Pianos Bar', 
    '335 Delancey Street', 
    'New York', 
    'NY', 
    '914-003-1132', 
    'https://www.facebook.com/theduelingpianos', 
    'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
);

INSERT INTO "Venue" (id, name,  address, city, state, phone, facebook_link,  image_link)
VALUES (
    3, 
    'Park Square Live Music & Coffee', 
    '34 Whiskey Moore Ave', 
    'San Francisco', 
    'CA', 
    '415-000-1234', 
    'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', 
    'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
);

INSERT INTO "Artist" (id,name,genres,city,state,phone,facebook_link,image_link)
VALUES (
    4, 
    'Guns N Petals', 
    ARRAY['Rock n Roll'], 
    'San Francisco', 
    'CA', 
    '326-123-5000', 
    'https://www.facebook.com/GunsNPetals', 
    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
);

INSERT INTO "Artist" (id,name,genres,city,state,phone,facebook_link,image_link)
VALUES (
    5, 
    'Matt Quevedo', 
    ARRAY['Jazz'], 
    'New York', 
    'NY', 
    '300-400-5000', 
    'https://www.facebook.com/mattquevedo923251523', 
    'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
);

INSERT INTO "Artist" (id,name,genres,city,state,phone,image_link)
VALUES (
    6, 
    'The Wild Sax Band', 
    ARRAY['Jazz', 'Classical'], 
    'San Francisco', 
    'CA', 
    '432-325-5432', 
    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
);



### comment out db.create_all()
### un comment new fields

flask db migrate
flask db upgrade


psql::::

UPDATE "Venue"
SET
    name = 'The Musical Hop',
    genres = ARRAY['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
    address = '1015 Folsom Street',
    city = 'San Francisco',
    state = 'CA',
    phone = '123-123-1234',
    website = 'https://www.themusicalhop.com',
    facebook_link = 'https://www.facebook.com/TheMusicalHop',
    seeking_talent = TRUE,
    seeking_description = 'We are on the lookout for a local artist to play every two weeks. Please call us.',
    image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
WHERE
    id = 1;

UPDATE "Venue"
SET
    name = 'The Dueling Pianos Bar',
    genres = ARRAY['Classical', 'R&B', 'Hip-Hop'],
    address = '335 Delancey Street',
    city = 'New York',
    state = 'NY',
    phone = '914-003-1132',
    website = 'https://www.theduelingpianos.com',
    facebook_link = 'https://www.facebook.com/theduelingpianos',
    seeking_talent = FALSE,
    image_link = 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
WHERE
    id = 2;

UPDATE "Venue"
SET
    name = 'Park Square Live Music & Coffee',
    genres = ARRAY['Rock n Roll', 'Jazz', 'Classical', 'Folk'],
    address = '34 Whiskey Moore Ave',
    city = 'San Francisco',
    state = 'CA',
    phone = '415-000-1234',
    website = 'https://www.parksquarelivemusicandcoffee.com',
    facebook_link = 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
    seeking_talent = FALSE,
    image_link = 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
WHERE
    id = 3;



UPDATE "Artist"
SET
    name = 'Guns N Petals',
    genres = ARRAY['Rock n Roll'],
    city = 'San Francisco',
    state = 'CA',
    phone = '326-123-5000',
    website = 'https://www.gunsnpetalsband.com',
    facebook_link = 'https://www.facebook.com/GunsNPetals',
    seeking_venue = TRUE,
    seeking_description = 'Looking for shows to perform at in the San Francisco Bay Area!',
    image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
WHERE
    id = 4;

UPDATE "Artist"
SET
    name = 'Matt Quevedo',
    genres = ARRAY['Jazz'],
    city = 'New York',
    state = 'NY',
    phone = '300-400-5000',
    facebook_link = 'https://www.facebook.com/mattquevedo923251523',
    seeking_venue = FALSE,
    image_link = 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
WHERE
    id = 5;

UPDATE "Artist"
SET
    name = 'The Wild Sax Band',
    genres = ARRAY['Jazz', 'Classical'],
    city = 'San Francisco',
    state = 'CA',
    phone = '432-325-5432',
    seeking_venue = FALSE,
    image_link = 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
WHERE
    id = 6;





### un comment shows fields and model

flask db migrate
flask db upgrade





INSERT INTO "Show" (venue_id, artist_id, start_time)
VALUES
    (1, 4, '2019-05-21T21:30:00.000Z'),
    (3, 5, '2019-06-15T23:00:00.000Z'),
    (3, 6, '2035-04-01T20:00:00.000Z'),
    (3, 6, '2035-04-08T20:00:00.000Z'),
    (3, 6, '2035-04-15T20:00:00.000Z');




pip install pycodestyle