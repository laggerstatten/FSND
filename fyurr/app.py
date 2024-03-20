# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    abort)
from flask import Response, flash
from models import db, Venue, Artist, Show
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import json
import dateutil.parser
import babel
import sys
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

migrate = Migrate(app, db)

# TO/DO: connect to a local postgresql database


# ----------------------------------------------------------------------------#
# Create all tables.
# ----------------------------------------------------------------------------#

# db.create_all()

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # TO/DO: replace with real venues data.
    # num_upcoming_shows should be aggregated
    # based on number of upcoming shows per venue.

    venues = Venue.query.all()
    data = []
    for venue in venues:
        data.append({
            "city": venue.city,
            "state": venue.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name,
            }]
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TO/DO: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop"
    # and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', '')
    search = "%{}%".format(search_term)
    venues = Venue.query.filter(Venue.name.ilike(search)).all()
    matched_venues = []
    for venue in venues:
        matched_venues.append({
            "id": venue.id,
            "name": venue.name,
        })

    response = {
        "count": len(venues),
        "data": matched_venues
    }

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TO/DO: replace with real venue data from the venues table, using venue_id

    # show_venue = Venue.query.get_or_404(venue_id)
    # data = vars(show_venue)

    show_venue = Venue.query.get_or_404(venue_id)

    past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time < datetime.now()
    ).\
        all()

    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time > datetime.now()
    ).\
        all()

    data = vars(show_venue)

    data['past_shows'] = [{
        'artist_id': artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
    } for artist, show in past_shows]

    data['upcoming_shows'] = [{
        'artist_id': artist.id,
        'artist_name': artist.name,
        'artist_image_link': artist.image_link,
        'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    } for artist, show in upcoming_shows]

    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TO/DO: insert form data as a new Venue record in the db, instead
    # TO/DO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form, meta={'csrf': False})

    # Validate all fields
    if form.validate():
        try:
            venue = Venue(name=form.name.data,
                          city=form.city.data,
                          state=form.state.data,
                          address=form.address.data,
                          phone=form.phone.data,
                          genres=form.genres.data,
                          facebook_link=form.facebook_link.data,
                          image_link=form.image_link.data,
                          website=form.website_link.data,
                          seeking_talent=form.seeking_talent.data,
                          seeking_description=form.seeking_description.data)
            db.session.add(venue)
            db.session.commit()
            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
        except ():
            # TO/DO: on unsuccessful db insert, flash an error instead.
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            db.session.rollback()
            flash('An error occurred. Venue ' +
                  request.form['name'] + ' could not be listed.')
            print(sys.exc_info())
        finally:
            db.session.close()
            return render_template('pages/home.html')

    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash('Please fix the following errors: ' + ', '.join(message))
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TO/DO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record.
    # Handle cases where the session commit could fail.

    venue = Venue.query.get(venue_id)
    if venue:
        try:
            db.session.delete(venue)
            db.session.commit()
            flash('Venue ' + venue.name + ' was successfully deleted!')
        except ():
            db.session.rollback()
            flash('An error occurred. Venue ' +
                  venue.name + ' could not be deleted.')
        finally:
            db.session.close()
            # return jsonify({ 'success': True })
            return None

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that
    # clicking that button delete it from the db
    # then redirect the user to the homepage


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TO/DO: replace with real data returned from querying the database

    artists = Artist.query.all()
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TO/DO: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals",
    # "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term', '')
    search = "%{}%".format(search_term)
    artists = Artist.query.filter(Artist.name.ilike(search)).all()
    matched_artists = []
    for artist in artists:
        matched_artists.append({
            "id": artist.id,
            "name": artist.name,
        })

    response = {
        "count": len(artists),
        "data": matched_artists
    }

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TO/DO: replace with real artist data
    # from the artist table, using artist_id

    # show_artist = Artist.query.get_or_404(artist_id)
    # data = vars(show_artist)

    show_artist = Artist.query.get_or_404(artist_id)

    past_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
        filter(
            Show.venue_id == Venue.id,
            Show.artist_id == artist_id,
            Show.start_time < datetime.now()
    ).\
        all()

    upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
        filter(
            Show.venue_id == Venue.id,
            Show.artist_id == artist_id,
            Show.start_time > datetime.now()
    ).\
        all()

    data = vars(show_artist)

    data['past_shows'] = [{
        'venue_id': venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
    } for venue, show in past_shows]

    data['upcoming_shows'] = [{
        'venue_id': venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    } for venue, show in upcoming_shows]

    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    # TODO: edit_artist: populate form with fields
    # from artist with ID <artist_id>
    artist_found = Artist.query.get(artist_id)

    # check if artist exists
    if not artist_found:
        return render_template('errors/404.html')

    artist = {
        "id": artist_found.id,
        "name": artist_found.name,
        "genres": artist_found.genres,
        "city": artist_found.city,
        "state": artist_found.state,
        "phone": artist_found.phone,
        "facebook_link": artist_found.facebook_link,
        "image_link": artist_found.image_link
    }

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TO/DO: edit_artist_submission: take values from the form submitted,
    # and update existing
    # artist record with ID <artist_id> using the new attributes

    artist = Artist.query.get(artist_id)
    # check if artist exists
    if not artist:
        return render_template('errors/404.html')

    artist.name = request.form['name']
    artist.genres = request.form['genres']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website']
    artist.seeking_venue = request.form['seeking_venue']
    artist.seeking_description = request.form['seeking_description']
    artist.image_link = request.form['image_link']
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
    db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    # TODO: edit_venue: populate form with values from venue with ID <venue_id>
    venue_found = Venue.query.get(venue_id)

    # check if venue exists
    if not venue_found:
        return render_template('errors/404.html')

    venue = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TO/DO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    venue = Venue.query.get(venue_id)
    # check if venue exists
    if not venue:
        return render_template('errors/404.html')

    venue.name = request.form['name']
    venue.genres = request.form['genres']
    venue.address = request.form['address']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.seeking_talent = request.form['seeking_talent']
    venue.seeking_description = request.form['seeking_description']
    venue.image_link = request.form['image_link']
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TO/DO: insert form data as a new Venue record in the db, instead
    # TO/DO: modify data to be the data object returned from db insertion
    form = ArtistForm(request.form, meta={'csrf': False})

    # Validate all fields
    if form.validate():
        try:
            artist = Artist(name=form.name.data,
                            city=form.city.data,
                            state=form.state.data,
                            phone=form.phone.data,
                            genres=form.genres.data,
                            facebook_link=form.facebook_link.data,
                            image_link=form.image_link.data,
                            website_link=form.website_link,
                            seeking_venue=form.seeking_venue,
                            seeking_description=form.seeking_description
                            )
            db.session.add(artist)
            db.session.commit()
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
        except ():
            # TO/DO: on unsuccessful db insert,
            # flash an error instead.
            db.session.rollback()
            flash('An error occurred. Artist ' +
                  request.form['name'] + ' could not be listed.')
            print(sys.exc_info())
        finally:
            db.session.close()
            return render_template('pages/home.html')

    # If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash('Please fix the following errors: ' + ', '.join(message))
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TO/DO: shows: replace with real venues data.

    shows = db.session.query(Show, Artist, Venue).join(Artist).join(
        Venue).filter(Show.start_time > datetime.now()).all()
    data = []
    for show in shows:
        data.append({
            "venue_id": show.Venue.id,
            "venue_name": show.Venue.name,
            "artist_id": show.Artist.id,
            "artist_name": show.Artist.name,
            "artist_image_link": show.Artist.image_link,
            "start_time": show.Show.start_time.strftime("%m/%d/%Y, %H:%M"),
        })

        return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db,
    # upon submitting new show listing form
    # TO/DO: create_show_submission: insert form data
    # as a new Show record in the db, instead

    form = ShowForm(request.form, meta={'csrf': False})

    # Validate all fields
    if form.validate():
        try:
            show = Show(
                venue_id=form.venue_id.data,
                artist_id=form.artist_id.data,
                start_time=form.start_time.data)
            db.session.add(show)
            db.session.commit()
            # on successful db insert, flash success
            flash('Show was successfully listed!')
        except ():
            # TO/DO: create_show_submission: on unsuccessful db insert,
            # flash an error instead.
            # e.g., flash('An error occurred. Show could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            db.session.rollback()
            flash('An error occurred. Show could not be listed.')
            print(sys.exc_info())
        finally:
            db.session.close()
            return render_template('pages/home.html')

    # If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash('Please fix the following errors: ' + ', '.join(message))
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('errors/401.html'), 401


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(422)
def not_processable_error(error):
    return render_template('errors/422.html'), 422


@app.errorhandler(405)
def invalid_method_error(error):
    return render_template('errors/405.html'), 405


@app.errorhandler(409)
def duplicate_resource_error(error):
    return render_template('errors/409.html'), 409


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
