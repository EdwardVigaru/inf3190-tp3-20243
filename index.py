# Copyright 2024 <Votre nom et code permanent>
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

from flask import Flask
from flask import render_template
from flask import g
from flask import request
from random import sample
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
    query = request.args.get('query', '').lower()
    animaux = get_db().get_animaux()
    resultats = [animal for animal in animaux if query in animal["nom"].lower() or query in animal["description"].lower()]
    return render_template('search.html', resultats = resultats, query = query)

@app.route('/adoption')
def adoption_form():
    return render_template('form.html')

@app.route('/adoption_submit')
def adoption_submit():
    data = request.form
    errors = []
    