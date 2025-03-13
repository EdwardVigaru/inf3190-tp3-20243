# Copyright 2024 <Vigaru Edward Ionutt>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, redirect, url_for
from flask import render_template
from flask import g
from flask import request
from random import sample
import re
from .database import Database

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():
    animaux = get_db().get_animaux()
    animaux_aleatoires = sample(animaux, 5)
    return render_template('index.html', animaux = animaux_aleatoires)

@app.route('/animal/<int:id>')
def animal(id):
    animal = get_db().get_animal(id)
    if not animal:
        return render_template('error.html', message = "Animal non trouvé"), 404
    return render_template('animal.html', animal = animal)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    db = get_db()
    
    try:
        animaux = db.get_animaux()
        for animal in animaux:
            if query == animal["nom"].lower():
                return redirect(url_for('animal', id=animal["id"]))
        
        return render_template('error.html', message=f"Aucun animal trouvé pour le nom '{query}'.")
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return render_template('error.html', message="Une erreur est survenue pendant la recherche.")


@app.route('/adoption')
def adoption_form():
    return render_template('form.html')

@app.route("/adoption_submit", methods=["POST"])
def adoption_submit():
    data = request.form
    errors = []

    fields_to_validate = {
        'nom': "Nom",
        'espece': "Espèce",
        'race': "Race",
        'description': "Description",
        'courriel': "Courriel",
        'adresse': "Adresse",
        'ville': "Ville",
        'cp': "Code postal"
    }

    def contains_comma(value):
        return ',' in value

    for field, label in fields_to_validate.items():
        value = data.get(field, '').strip()
        if contains_comma(value):
            errors.append(f"Le champ '{label}' ne peut pas contenir de virgule.")

    if not (3 <= len(data.get('nom', '').strip()) <= 20):
        errors.append("Le nom de l'animal doit comporter entre 3 et 20 caractères.")
    if not data.get('age', '').isdigit() or not (0 <= int(data.get('age')) <= 30):
        errors.append("L'âge doit être un nombre entre 0 et 30.")
    if not re.match(r'^\S+@\S+\.\S+$', data.get('courriel', '').strip()):
        errors.append("L'adresse courriel n'est pas valide.")
    if not re.match(r'^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$', data.get('cp', '').strip()):
        errors.append("Le code postal doit être au format canadien (ex. H3Z 2Y7).")

    if errors:
        return render_template("form.html", title="Mise en adoption", errors=errors, form_data=data)

    try:
        db = get_db()
        animal_id = db.add_animal(
            nom=data['nom'].strip(),
            espece=data['espece'].strip(),
            race=data['race'].strip(),
            age=int(data['age']),
            description=data['description'].strip(),
            courriel=data['courriel'].strip(),
            adresse=data['adresse'].strip(),
            ville=data['ville'].strip(),
            cp=data['cp'].strip().upper()
        )
        return redirect(url_for("animal", id=animal_id))
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'animal : {e}")
        errors.append("Une erreur est survenue lors de l'ajout. Veuillez réessayer.")
        return render_template("form.html", title="Mise en adoption", errors=errors, form_data=data)
    
@app.route('/liste')
def liste_animaux():
    animaux = get_db().get_animaux()
    return render_template('liste.html', animaux=animaux)
