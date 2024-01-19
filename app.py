# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model.
Base = automap_base()
# Reflect the tables.
Base.prepare(engine, reflect=True)

# Save reference to the tables.
Measurement = Base.classes.measurement
Station = Base.classes.station
# print(Base.classes.keys())
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    routes = []
    
    # Add the available routes to the list
    routes.append("/")
    routes.append("/api/v1.0/precipitation")
    routes.append("/api/v1.0/stations")
    routes.append("/api/v1.0/tobs")
    routes.append("/api/v1.0/<start>")
    routes.append("/api/v1.0/<start>/<end>")
    
    # Return the list of available routes
    return jsonify(routes)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 12 months ago from the last date in the database
    last_year_date = dt.date.today() - dt.timedelta(days=365)
    
    # Perform the query to retrieve the precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp)\
                     .filter(Measurement.date >= last_year_date)\
                     .all()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp
    
    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)
    
    #session.close()


@app.route("/api/v1.0/stations")
def stations():
    # Perform the query to retrieve the list of stations
    results = session.query(Station.station).all()
    
    # Convert the query results to a list
    station_list = [result[0] for result in results]
    
    # Return the JSON representation of the list
    return jsonify(station_list)
    
   #session.close()


@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 12 months ago from the last date in the database
    last_year_date = dt.date.today() - dt.timedelta(days=365)
    
    # Perform the query to retrieve the dates and temperature observations
    # of the most active station for the previous year of data
    results = session.query(Measurement.date, Measurement.tobs)\
                     .filter(Measurement.station == most_active_station)\
                     .filter(Measurement.date >= last_year_date)\
                     .all()
    
    # Create a list of dictionaries with date and tobs as keys
    tobs_data = []
    for date, tobs in results:
        tobs_data.append({"date": date, "tobs": tobs})
    
    # Return the JSON representation of the list
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    # Perform the query to calculate the minimum, average, and maximum temperatures
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs))\
                     .filter(Measurement.date >= start)\
                     .all()
    
    # Create a dictionary with the temperature statistics
    temperature_stats = {
        "start_date": start,
        "end_date": None,
        "min_temperature": results[0][0],
        "avg_temperature": results[0][1],
        "max_temperature": results[0][2]
    }
    
    # Return the JSON representation of the dictionary
    return jsonify(temperature_stats)


@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
    # Perform the query to calculate the minimum, average, and maximum temperatures
    results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs))\
                     .filter(Measurement.date >= start)\
                     .filter(Measurement.date <= end)\
                     .all()
    
    # Create a dictionary with the temperature statistics
    temperature_stats = {
        "start_date": start,
        "end_date": end,
        "min_temperature": results[0][0],
        "avg_temperature": results[0][1],
        "max_temperature": results[0][2]
    }
    
    # Return the JSON representation of the dictionary
    return jsonify(temperature_stats)


session.close()

if __name__ == "__main__":
    app.run(debug=True)