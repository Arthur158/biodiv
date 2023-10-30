from flask import Flask, jsonify, request, render_template, redirect, url_for, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from classes.climate import Climate
from classes.diet import Trophic_type

from classes.planet import Planet
from classes.population import Population
from classes.region import Region
from classes.species import Species
from constants import SPECIES_IMAGE_FOLDER
from name_generator import get_random_name, get_random_region_name

app = Flask(__name__)
planet = Planet()

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)


@app.route('/')
def index():
    return render_template('welcome.html', status=planet.status.value)


@app.route('/add_region', methods=['GET', 'POST'])
def add_region():

    if request.method == 'POST':
        name = request.form.get('name')
        climate = request.form.get('climate')

        if name and climate:
            planet.add_region(Region(name, Climate(climate)))
            return redirect(url_for('add_region'))
        
    regions= planet.db_handler.execute_sql_query("SELECT name, climate FROM regions")

    return render_template('add_region.html', regions=regions, status=planet.status.value, year=planet.year)


@app.route('/add_species', methods=['GET', 'POST'])
def add_species():
    if request.method == 'POST':
        name = request.form.get('name')
        trophic_type = request.form.get('trophic_type')

        if name and trophic_type:
            heterotroph_level = None
            if trophic_type == 'heterotrophic':
                heterotroph_level = request.form.get('heterotroph_level')

            planet.db_handler.insert_species(name,trophic_type, heterotroph_level)
            return redirect(url_for('add_species'))

    species = planet.db_handler.execute_sql_query("SELECT name,trophic_type,heterotroph_level FROM species")
    return render_template('add_species.html', species=species, status=planet.status.value, year=planet.year)


@app.route('/region/<region_name>', methods=['GET', 'POST'])
def show_region(region_name):

    region = planet.db_handler.execute_sql_query("SELECT name, climate FROM regions WHERE regions.name = ?", (region_name))
    #for future uses.

    populations = planet.db_handler.execute_sql_query("SELECT populations.species, populations.population_size, species.trophic_type, species.heterotroph_level, populations.id FROM populations JOIN species ON species.name == populations.species WHERE populations.region = ?", (region_name,))

    species_names = planet.db_handler.execute_sql_query("SELECT name FROM species")

    return render_template('region.html', region_name=region_name, populations=populations, species=species_names, status=planet.status.value, year=planet.year)


@app.route('/region/add', methods=['POST'])
def register_population():

    region_name = request.form.get('region_name')
    species = request.form.get('species')
    population_size = request.form.get('population_size')

    planet.db_handler.insert_population(species, population_size, region_name)

    return "correctly added the population"


@app.route('/species/<species_name>', methods=['GET', 'POST'])
def show_species(species_name):

    species = planet.db_handler.execute_sql_query("SELECT name, trophic_type, heterotroph_level FROM species WHERE species.name == ?", (species_name,))[0]
    populations = planet.db_handler.execute_sql_query("SELECT population_size, region, id FROM populations WHERE populations.species = ?", (species_name,))

    if request.method == 'POST':
        image = request.files['file']
        image.save(os.path.join(SPECIES_IMAGE_FOLDER, f"{species_name}.jpg"))

    image_exists = os.path.exists(os.path.join(SPECIES_IMAGE_FOLDER, f"{species_name}.jpg"))

    return render_template('species.html', populations= populations, image_exists=image_exists, species_name=species_name, trophic_type=species[1], heterotrophic_level=species[2], status=planet.status.value, year=planet.year)


@app.route('/population/<region_name>/<species_name>', methods=['GET'])
def show_population(region_name, species_name):

    population = planet.db_handler.execute_sql_query("SELECT species, population_size, region FROM populations WHERE populations.region = ? AND populations.species = ?", (region_name, species_name))[0]
    
    image_exists = os.path.exists(os.path.join(SPECIES_IMAGE_FOLDER, f"{population[0]}.jpg"))

    return render_template('population.html', image_exists= image_exists, species_name = population[0], population_size = population[1], region_name = region_name, status=planet.status.value)


@app.route('/delete/<region_name>/<species_name>', methods=['GET'])
def delete_population(region_name, species_name):

    planet.db_handler.delete_population(region_name, species_name)

    return f"Successfully removed population of {species_name} from the region {region_name}."

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


@app.route("/save", methods=['GET'])
def save_simulation():
    planet.save_simulation()
    return "Successfully stopped the simulation."


@app.route("/skip", methods=['GET'])
def skip():

    planet.get_from_database()

    planet.execute_generation()

    planet.save_simulation()
    
    return "Successfully executed a generation"

@app.route("/remove-all", methods=['GET'])
def remove_all():

    planet.db_handler.remove_all()
    return "Succesfullly removed all tables"

if __name__ == '__main__':

    planet.get_from_database()
    app.run(debug=True)
