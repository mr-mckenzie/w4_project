from db.run_sql import run_sql

from models.location import Location
import repositories.country_repository as country_repo

def save (location : Location):
    sql = 'INSERT INTO locations (name, country_id) VALUES (%s, %s) RETURNING id'
    values = (location.name, location.country.id)
    result = run_sql(sql, values)
    location.id = result[0]['id']
    return location

def select_all():
    sql = 'SELECT * FROM locations'
    results = run_sql(sql)
    location_list = [ ]
    for row in results:
        location_country = country_repo.select_one(row[2])
        new_location = Location(row[1], location_country, int(row[0]))
        location_list.append(new_location)
    #    print(row['name'])
    return location_list

def select_one(location_id):
    sql = 'SELECT * FROM locations WHERE id = (%s)'
    value = str(location_id)
    result = run_sql(sql, value)[0]
    selected_country = country_repo.select_one(result[2])
    selected_location = Location(result[1], selected_country, int(result[0]))
    return selected_location