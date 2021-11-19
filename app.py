#Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Adding flask dependency 
from flask import Flask, jsonify

#Setting up database engine
#Allows us to access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflecting our tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#Creating variabbles for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station


#Creating a session link
session = Session(engine)


#Creating a new flask app instance
#Instance is the general term for refering to a singular version of something
app = Flask(__name__)
#__name__ 


#This "@app.route('/')" is the starting point or the root of the route
#the '/' indicates the highest level of hierarchy in any computer system directory
#All routes should go after the app = Flask(__name__) 
@app.route('/')

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
#Precipitation route
@app.route("/api/v1.0/precipitation")

#return jsonify(variable) to return in a json format
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    #make it into a dictionary so it can be jsonified
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#Stations route
@app.route("/api/v1.0/stations")

def stations():
    #Write a query that calls all stations into the database
    results = session.query(Station.station).all()
    #Convert this into a list so we can jsonify it
    stations = list(np.ravel(results))
    return jsonify(stations)

# Temperature route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    # Calculate one year before the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Query the station temp readings over the course of a year
    results= session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    #Convert into list for jsonify
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Add parameters start and end
def stats(start=None, end=None):
    #A query to pick out the min, max, and avg temps in the database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)