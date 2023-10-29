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
        
    regions= [(region.name, region.climate.value) for region in planet.regions.values()]

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

            planet.add_species(Species(name, Trophic_type(trophic_type), heterotroph_level))
            return redirect(url_for('add_species'))

    # species = [
    #     (
    #         specie.name, 
    #         specie.trophic_type.value, 
    #         int(specie.heterotroph_level) if specie.heterotroph_level is not None else None
    #     ) 
    #     for specie in planet.species.values()
    # ]

    species = planet.db_handler.execute_sql_query("SELECT name,trophic_type,heterotroph_level FROM species")
    return render_template('add_species.html', species=species, status=planet.status.value, year=planet.year)


@app.route('/region/<region_name>', methods=['GET', 'POST'])
def show_region(region_name):

    # breakpoint()
    region = planet.regions.get(region_name)
    if not region:
        return "Region not found", 404


    # species_names = [specie.name for specie in planet.species.values()]

    # populations = [
    #     (
    #         population.species.name, 
    #         population.population_size, 
    #         population.species.trophic_type.value, 
    #         int(population.species.heterotroph_level) if population.species.heterotroph_level is not None else None
    #     ) 
    #     for population in region.populations.values()
    # ]

    # breakpoint()
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
    species = planet.species.get(species_name)
    if not species:
        return "Species not found", 404

    if request.method == 'POST':
        image = request.files['file']
        image.save(os.path.join(SPECIES_IMAGE_FOLDER, f"{species_name}.jpg"))

    image_exists = os.path.exists(os.path.join(SPECIES_IMAGE_FOLDER, f"{species_name}.jpg"))

    return render_template('species.html', image_exists=image_exists, species_name=species.name, trophic_type=species.trophic_type.value, heterotrophic_level=species.heterotroph_level, status=planet.status.value, year=planet.year)


@app.route('/population/<region_name>/<species_name>', methods=['GET'])
def show_population(region_name, species_name):

    population: Population = planet.regions.get(region_name).populations.get(species_name)

    image_exists = os.path.exists(os.path.join(SPECIES_IMAGE_FOLDER, f"{population.species.name}.jpg"))

    return render_template('population.html', image_exists= image_exists, species_name = population.species.name, population_size = population.population_size, region_name = region_name, status=planet.status.value)


@app.route('/delete/<region_name>/<species_name>', methods=['GET'])
def delete_population(region_name, species_name):

    planet.regions.get(region_name).populations.pop(species_name)
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

    planet.empty_out()
    planet.get_from_database()

    # breakpoint()


    planet.execute_generation()

    # breakpoint()

    planet.save_simulation()
    planet.get_from_database()
    
    # breakpoint()

    return "Successfully executed a generation"

@app.route("/remove-all", methods=['GET'])
def remove_all():
    planet.db_handler.remove_all()
    planet.start_simulation()
    return "Succesfullly removed all tables"

if __name__ == '__main__':

    planet.get_from_database()
    app.run(debug=True)
