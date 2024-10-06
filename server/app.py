#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    # Query the earthquake by ID
    earthquake = Earthquake.query.get(id)
    
    # If earthquake is not found, return an error response
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    
    # If earthquake is found, return the details as JSON
    return jsonify({
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    })

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query earthquakes with magnitude >= provided value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare the list of matching earthquakes
    quakes = [{
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
    } for quake in earthquakes]
    
    # Return the count and the list in JSON format
    return jsonify({
        "count": len(earthquakes),
        "quakes": quakes
    }), 200



if __name__ == '__main__':
    app.run(port=5555, debug=True)
