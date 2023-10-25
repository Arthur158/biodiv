from flask import Flask, jsonify, request, render_template, request, redirect, send_from_directory, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

import sqlite3

from classes.planet import Planet
from classes.region import Region
from constants import DATABASE_NAME, SPECIES_IMAGE_FOLDER, STRINGS_TO_CLIMATES
from database_handler import DatabaseHandler
from errors import InputError
from name_generator import get_random_name, get_random_region_name

app = Flask(__name__)
db_handler = DatabaseHandler()
planet = Planet()

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/add_region', methods=['GET', 'POST'])
def add_region():
    if request.method == 'POST':
        name = request.form.get('name')
        climate = request.form.get('climate')

        if name and climate:  # Basic validation
            try:
               db_handler.insert_region(name, climate) 
            except Exception as e:  # General exception for demo; specify exceptions for production
                print(f"An error occurred: {e}")

            # Redirect to the same add_region page to prevent form resubmission issues
            return redirect(url_for('add_region'))
                
    regions = db_handler.execute_sql_query("SELECT name, climate FROM regions")

    return render_template('add_region.html', regions= regions)

@app.route('/add_species', methods=['GET', 'POST'])
def add_species():
    if request.method == 'POST':
        # Using get() to fetch form data. This will return None if the key doesn't exist.
        name = request.form.get('name')
        trophic_type = request.form.get('trophic_type')  # This will get the value "Autotroph" or "Heterotroph"

        if name and trophic_type:
            # If Heterotroph is selected, fetch the slider value as well
            heterotroph_level = None
            if trophic_type == 'heterotrophic':
                heterotroph_level = request.form.get('heterotroph_level')  # This will get the value from the slider

            db_handler.insert_species(name,trophic_type, heterotroph_level)

        # Redirect to the same add_species page to prevent form resubmission issues
        return redirect(url_for('add_species'))
                
    species = db_handler.execute_sql_query("SELECT name, trophic_type, heterotroph_level FROM species")

    return render_template('add_species.html', species=species)

@app.route('/region/<region>', methods=['GET', 'POST'])
def show_region(region):

    if request.method == 'POST':
        # Using get() to fetch form data. This will return None if the key doesn't exist.
        name = request.form.get('species')
        population_size = request.form.get('population_size')

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO populations (species, population_size, region) VALUES (?, ?, ?)", (name.split("'")[1], population_size, region))
            conn.commit()
            msg = "population successfully added!"
        except Exception as e:
            conn.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            conn.close()

        # Redirect to the same add_species page to prevent form resubmission issues
        return redirect(url_for('show_region', region=region))
    populations = db_handler.execute_sql_query("SELECT populations.population_size, populations.species, species.trophic_type, species.heterotroph_level, populations.id FROM populations JOIN species ON species.name == populations.species WHERE populations.region = ?", (region,))

    species = db_handler.execute_sql_query("SELECT name FROM species")

    return render_template('region.html', region_name= region,  populations= populations, species=species)

@app.route('/population/<population_id>', methods=['GET'])
def show_population(population_id):

    population = db_handler.execute_sql_query("SELECT species, population_size, region FROM populations WHERE populations.id == ?", (population_id,))[0]

    image_exists = os.path.exists(os.path.join(SPECIES_IMAGE_FOLDER, f"{population[0]}.jpg"))

    return render_template('population.html', image_exists= image_exists, species_name = population[0], population_size = population[1], region_name = population[2])

@app.route('/species/<species_name>', methods=['GET','POST'])
def show_species(species_name):

    if request.method == 'POST':
        image = request.files['file']
        image.save(os.path.join(SPECIES_IMAGE_FOLDER, f"{species_name}.jpg"))

    species = db_handler.execute_sql_query("SELECT name, trophic_type, heterotroph_level FROM species WHERE species.name == ?", (species_name,))[0]
    print(species)
    populations = db_handler.execute_sql_query("SELECT population_size, region, id FROM populations WHERE populations.species = ?", (species_name,))

    image_exists = os.path.exists(os.path.join(SPECIES_IMAGE_FOLDER, f"{species_name}.jpg"))
    
    return render_template('species.html', image_exists = image_exists, species_name = species[0], trophic_type = species[1], heterotrophic_level=species[2], populations= populations)
     
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return redirect(url_for('show', filename=filename))

    return render_template('upload_form.html')

   
@app.route('/uploads/<filename>')
def show(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/randomize_name', methods=['GET'])
def randomize_name():
    return jsonify(get_random_name())

@app.route('/randomize_region_name', methods=['GET'])
def randomize_region_name():
    return jsonify(get_random_region_name())

@app.route('/remove_all', methods=['GET'])
def remove_all():
    # Connect to the SQLite database
    db_handler.remove_all()

    return "Successfully removed all entries from all tables."

@app.route('/start', methods=['GET'])
def start_simulation():
    planet.start_simulation()
    return "Successfully started the simulation."


@app.route("/stop", methods=['GET'])
def stop_simulation():
    planet.stop_simulation()
    return "Successfully stopped the simulation."


if __name__ == '__main__':
    app.run(debug=True)


