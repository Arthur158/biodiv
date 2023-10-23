from flask import Flask, request, render_template, request, redirect, url_for, g
import sqlite3

from classes.planet import Planet
from classes.region import Region
from constants import DATABASE_NAME, STRINGS_TO_CLIMATES
from errors import InputError

app = Flask(__name__)

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
                print(name + "and" + climate)
                # Uncomment if you want to use g.planet and custom exception
                # g.planet.add_region(Region(name, STRINGS_TO_CLIMATES[climate]))
                conn = sqlite3.connect(DATABASE_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO regions (name, climate) VALUES (?, ?)", (name, climate))
                conn.commit()
                conn.close()
            except Exception as e:  # General exception for demo; specify exceptions for production
                print(f"An error occurred: {e}")

            # Redirect to the same add_region page to prevent form resubmission issues
            return redirect(url_for('add_region'))
                
    # Fetch regions from the database
    conn = sqlite3.connect('planet.db')
    c = conn.cursor()
    c.execute("SELECT name, climate FROM regions")
    regions = c.fetchall()
    conn.close()

    return render_template('add_region.html', regions= regions)

@app.route('/add_species', methods=['GET', 'POST'])
def add_species():
    if request.method == 'POST':
        # Using get() to fetch form data. This will return None if the key doesn't exist.
        name = request.form.get('name')

        # Fetching checkboxes' values and aggregating them
        trophic_types = request.form.getlist('trophic_type')  # This will return a list of checked values, like ['carnivore', 'herbivore']
        print(trophic_types)
        print("")
        aggregated_trophic_type = ", ".join(trophic_types)

        conn = sqlite3.connect("planet.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO species (name, trophic_type) VALUES (?, ?)", (name, aggregated_trophic_type))
            conn.commit()
            msg = "Species successfully added!"
        except Exception as e:
            conn.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            conn.close()

        # Redirect to the same add_species page to prevent form resubmission issues
        return redirect(url_for('add_species'))
                
    # Fetch regions from the database
    conn = sqlite3.connect('planet.db')
    c = conn.cursor()
    c.execute("SELECT name, trophic_type FROM species")
    species = c.fetchall()
    conn.close()

    return render_template('add_species.html', species= species)



if __name__ == '__main__':
    app.run(debug=True)


