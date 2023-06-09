# import flask
from flask import Flask, render_template, Blueprint, request, redirect
from models.location import Location
from models.location import Country
import repositories.continent_repository as continent_repo
import repositories.location_repository as location_repo
import repositories.country_repository as country_repo

countries_blueprint = Blueprint("countries", __name__)

#show all countries
@countries_blueprint.route('/countries')
def view_all_countries():
    all_countries = continent_repo.all_by_continent()
    continents = continent_repo.select_all()
    return render_template('countries/index.jinja', input_countries = all_countries, continents = continents)

#add a country
@countries_blueprint.route('/countries', methods=['POST'])
def add_a_country():
    new_country_name =request.form['name']
    continent_id = request.form['continent_id']
    continent = continent_repo.select_one(continent_id)

    #print(f'THIS IS NEW COUNTRY NAME: {new_country_name}')
    new_country = Country(new_country_name, continent)
    #print(f'THIS IS NEW COUNTRY INSTANCE: {new_country.__dict__}')
    country_repo.save(new_country)
    return redirect('/countries')

#show a single country and list all locations in country
@countries_blueprint.route('/countries/<id>')
def view_single_country(id):
    current_country = country_repo.select_one(id)
    all_locations = country_repo.get_locations(id)
    #print(all_locations)
    return render_template('/countries/locations.jinja', input_locations = all_locations, input_country = current_country)

#delete a country
@countries_blueprint.route('/countries/<id>/delete', methods=['POST'])
def delete_country(id):
    country_repo.delete_by_id(id)
    return redirect('/countries')

#go to edit country form
@countries_blueprint.route('/countries/<id>/edit', methods=['GET'])
def edit_country(id):
    current_country = country_repo.select_one(id)
    all_locations = country_repo.get_locations(id)
    return render_template('/countries/edit.jinja', input_locations = all_locations, input_country = current_country)

#change country name
@countries_blueprint.route('/countries/<id>/edit', methods=['POST'])
def edit_country_name(id):
    new_name = request.form['name']
    country_repo.update_name(id, new_name)
    path = '/countries/'+str(id)+'/edit'
    return redirect(path)

#add a location to a country
@countries_blueprint.route('/countries/<id>/add_location', methods=['POST'])
def add_location(id):
    new_location_name = request.form['name']
    #print(f'THIS IS NEW COUNTRY NAME: {new_location_name}')
    new_country_id = (request.form['country_id'])
    #print(f'THIS IS NEW COUNTRY INSTANCE: {new_country_id}')
    new_country = country_repo.select_one(new_country_id)
    new_location = Location(new_location_name, new_country)
    location_repo.save(new_location)
    path = '/countries/'+str(id)+'/edit'
    return redirect(path)