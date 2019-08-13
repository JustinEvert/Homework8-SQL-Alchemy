#Dependencies
import numpy as np
import pandas as pd
import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect

# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 1. Import Flask
from flask import Flask, jsonify


# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
     
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )      

@app.route("/api/v1.0/precipitation")
def precipitation():
# Create a session (link) from Python to the DB
    session = Session(engine)
    
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query same one year time-frame from step 1
    rain_query = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= query_date).all()
    
    session.close()
    
    daily_rain_dict = dict(rain_query)
    
    return jsonify(daily_rain_dict) 


@app.route("/api/v1.0/stations")
def stations():
# Create a session (link) from Python to the DB
    session = Session(engine)
    
# Query station names/numbers
    station_query = session.query(Station.station, Station.name).all()
    
    session.close()
    
# Convert list of tuples into normal list
    station_list = list(np.ravel(station_query))
 
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
# Create a session (link) from Python to the DB
    session = Session(engine)
    
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
# Query same one year time-frame from step 1
    temp_query = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date >= query_date).all()
    
    session.close()
    
# Convert list of tuples into normal list
    temp_list = list(np.ravel(temp_query))
 
    return jsonify(temp_list)




if __name__ == "__main__":
    app.run(debug=True)
