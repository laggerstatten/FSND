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
from models import app, db, Animal, Institution, Specimen
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
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

current_role = None
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)



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

# TODO update endpoints

#  Animals
#  ----------------------------------------------------------------
@app.route('/animals')
# @requires_auth('get:animal')
def animals():
    animals = Animal.query.all()

    return render_template(
        'pages/animals.html', 
        animals=animals)


#  Animals -- Search
#  ----------------------------------------------------------------
@app.route('/animals/search', methods=['POST'])
def search_animals():

    search_term = request.form.get('search_term', '')
    search = "%{}%".format(search_term)
    animals = Animal.query.filter(
        db.or_(
        Animal.genus.ilike(search)
        )
    ).all()

    matched_animals = []
    for animal in animals:
        matched_animals.append({
            "id": animal.id,
            "genus": animal.genus,
            "species": animal.species
        })

    response = {
        "count": len(animals),
        "data": matched_animals
    }

    return render_template(
        'pages/search_animals.html',
        results=response,
        search_term=request.form.get('search_term', ''))


#  Animals -- Individual Record
#  ----------------------------------------------------------------
@app.route('/animals/<int:animal_id>')
# @requires_auth(permission='read')
def show_animal(animal_id):
    show_animal = Animal.query.get_or_404(animal_id)

    data = vars(show_animal)

    return render_template(
        'pages/show_animals.html', 
        animal=data)


#  Animals -- Create
#  ----------------------------------------------------------------
@app.route('/animals/create', methods=['GET'])
def create_animal_form():
    form = AnimalForm()
    return render_template(
        'forms/new_animals.html', 
        form=form)


@app.route('/animals/create', methods=['POST'])
def create_animal_submission():
    form = AnimalForm(request.form, meta={'csrf': False})

    # Validate all fields
    if form.validate():
        try:
            animal = Animal(
                genus=form.genus.data,
                species=form.species.data
                )
            db.session.add(animal)
            db.session.commit()
            # on successful db insert, flash success
            flash('Animal ' +
                  ' was successfully listed!')
        except ():
            db.session.rollback()
            flash('An error occurred. Animal ' +
                  ' could not be listed.')
            print(sys.exc_info())
        finally:
            db.session.close()
            return render_template(
                'pages/home.html')

    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash('Please fix the following errors: ' + ', '.join(message))
        form = AnimalForm()
        return render_template(
            'forms/new_animal.html', 
            form=form)


#  Animals -- Update
#  ----------------------------------------------------------------
@app.route('/animals/<int:animal_id>/edit', methods=['GET'])
def edit_animal(animal_id):
    form = AnimalForm()

    animal_found = Animal.query.get(animal_id)

    # check if animal exists
    if not animal_found:
        return render_template('errors/404.html')

    animal = {
        "id": animal_found.id,
        "genus": animal_found.genus,
        "species": animal_found.species
    }

    return render_template(
        'forms/edit_animals.html', 
        form=form, 
        animal=animal)


@app.route('/animals/<int:animal_id>/edit', methods=['POST'])
def edit_animal_submission(animal_id):
    animal = Animal.query.get(animal_id)
    # check if animal exists
    if not animal:
        return render_template('errors/404.html')

    animal.genus = request.form['genus']

    try:
        db.session.commit()
        flash('Animal with ID {} was successfully updated!'.format(animal.id))
    except:
        db.session.rollback()
        flash('An error occurred. Animal with ID {} could not be updated.'.format(animal.id))
    finally:
        db.session.close()

    return redirect(url_for(
        'show_animal', 
        animal_id=animal_id))


#  Animals -- Delete
#  ----------------------------------------------------------------
@app.route('/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    deleted_animal = Animal.query.get(animal_id)
    
    try:
        db.session.delete(deleted_animal)
        db.session.commit()
        flash('Animal ' + ' was successfully deleted!')
    except:
        db.session.rollback()
        flash('Please try again. Animal ' + ' could not be deleted.')
    finally:
        db.session.close()

    return jsonify({'success': True})





#  Institutions
#  ----------------------------------------------------------------
@app.route('/institutions')
def institutions():
    institutions = Institution.query.all()

    return render_template(
        'pages/institutions.html', 
        institutions=institutions)


#  Institutions -- Search
#  ----------------------------------------------------------------
@app.route('/institutions/search', methods=['POST'])
def search_institutions():

    search_term = request.form.get('search_term', '')
    search = "%{}%".format(search_term)
    institutions = Institution.query.filter(
        db.or_(
            Institution.name.ilike(search)
        )
    ).all()

    matched_institutions = []
    for institution in institutions:
        matched_institutions.append({
            "id": institution.id,
            "name": institution.name
        })

    response = {
        "count": len(institutions),
        "data": matched_institutions
    }

    return render_template(
        'pages/search_institutions.html',
        results=response,
        search_term=request.form.get('search_term', ''))


#  Institutions -- Individual Record
#  ----------------------------------------------------------------
@app.route('/institutions/<int:institution_id>')
def show_institution(institution_id):
    show_institution = Institution.query.get_or_404(institution_id)

    data = vars(show_institution)

    return render_template(
        'pages/show_institutions.html', 
        institution=data)


#  Institutions -- Create
#  ----------------------------------------------------------------
@app.route('/institutions/create', methods=['GET'])
def create_institution_form():
    form = InstitutionForm()
    return render_template(
        'forms/new_institutions.html', 
        form=form)


@app.route('/institutions/create', methods=['POST'])
def create_institution_submission():
    form = InstitutionForm(request.form, meta={'csrf': False})

    # Validate all fields
    if form.validate():
        try:
            institution = Institution(
                name=form.name.data
                )
            db.session.add(institution)
            db.session.commit()
            # on successful db insert, flash success
            flash('Institution ' +
                  ' was successfully listed!')
        except ():
            db.session.rollback()
            flash('An error occurred. Institution ' +
                  ' could not be listed.')
            print(sys.exc_info())
        finally:
            db.session.close()
            return render_template(
                'pages/home.html')

    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash('Please fix the following errors: ' + ', '.join(message))
        form = InstitutionForm()
        return render_template(
            'forms/new_institution.html', 
            form=form)


#  Institutions -- Update
#  ----------------------------------------------------------------
@app.route('/institutions/<int:institution_id>/edit', methods=['GET'])
def edit_institution(institution_id):
    form = InstitutionForm()

    institution_found = Institution.query.get(institution_id)

    # check if institution exists
    if not institution_found:
        return render_template('errors/404.html')

    institution = {
        "id": institution_found.id,
        "name": institution_found.name
    }

    return render_template(
        'forms/edit_institutions.html', 
        form=form, 
        institution=institution)


@app.route('/institutions/<int:institution_id>/edit', methods=['POST'])
def edit_institution_submission(institution_id):
    institution = Institution.query.get(institution_id)
    # check if institution exists
    if not institution:
        return render_template('errors/404.html')

    institution.name = request.form['name']

    try:
        db.session.commit()
        flash('Institution {} was successfully updated!'.format(institution.name))
    except:
        db.session.rollback()
        flash('An error occurred. Institution {} could not be updated.'.format(institution.name))
    finally:
        db.session.close()

    return redirect(url_for(
        'show_institution', 
        institution_id=institution_id))


#  Institutions -- Delete
#  ----------------------------------------------------------------
@app.route('/institutions/<int:institution_id>', methods=['DELETE'])
def delete_institution(institution_id):
    deleted_institution = Institution.query.get(institution_id)
    
    try:
        db.session.delete(deleted_institution)
        db.session.commit()
        flash('Institution ' + ' was successfully deleted!')
    except:
        db.session.rollback()
        flash('Please try again. Institution ' + ' could not be deleted.')
    finally:
        db.session.close()

    return jsonify({'success': True})
    
    
    
    


















#  Specimens
#  ----------------------------------------------------------------
@app.route('/specimens')
def specimens():
    specimens = db.session.query(Specimen).\
        options(joinedload(Specimen.animal), joinedload(Specimen.institution)).all()
    
    data = []
    for specimen in specimens:
        data.append({
            "specimen_id": specimen.id,
            "institution_id": specimen.institution.id,
            "institution_name": specimen.institution.name,
            "animal_id": specimen.animal.id,
            "animal_genus": specimen.animal.genus,
            "sightingdate": specimen.sightingdate.strftime('%Y-%m-%d %H:%M:%S')
        })

    return render_template(
        'pages/specimens.html',
        specimens=data)


#  Specimens -- Create
#  ----------------------------------------------------------------
@app.route('/specimens/create', methods=['GET'])
def create_specimen_form():
    form = SpecimenForm()
    return render_template(
        'forms/new_specimen.html',
        form=form)


@app.route('/specimens/create', methods=['POST'])
def create_specimen_submission():
    form = SpecimenForm(request.form, meta={'csrf': False})

    # Validate all fields
    if form.validate():
        try:
            specimen = Specimen(
                institution_id=form.institution_id.data,
                animal_id=form.animal_id.data,
                sightingdate=form.sightingdate.data)
            db.session.add(specimen)
            db.session.commit()
            # on successful db insert, flash success
            flash('Specimen ' +
                  ' was successfully listed!')
        except ():
            db.session.rollback()
            flash('An error occurred. Specimen ' +
                  ' could not be listed.')
            print(sys.exc_info())
        finally:
            db.session.close()
            return render_template(
                'pages/home.html')

    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash('Please fix the following errors: ' + ', '.join(message))
        form = SpecimenForm()
        return render_template(
            'forms/new_specimen.html', 
            form=form)


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
