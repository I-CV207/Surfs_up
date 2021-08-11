#import Flask dependency
import datetime as dt
import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, engine, func
from flask import Flask, jsonify

#Set up engine variable to access andm query the Data Base file
engine=create_engine("sqlite:///hawaii.sqlite")

#Reflect the database into our classes
Base=automap_base()
Base.prepare(engine,reflect=True)
#Create variables from each of our classes to reference thjem later
Measurement=Base.classes.measurement
Station=Base.classes.station
#Create a session link from Python to our database
session=Session(engine)

#SET UP FLASK

#We will add a new Flask app instance
app=Flask(__name__)
#We define the starting point or root
@app.route("/")
#The '/'  denotes that we want to put our data at the root of out routes. The forward slah is commonly known as the highest level of hierearchy in any computer system

#Create a function
#When creating routes the convention is '/api/v1.0/' folowed by the name of the route. This signifies thath is version 1 of the application
def welcome():
    return(''' 
     Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end       
    ''')
#Create a precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year=dt.date(2017,8,23)-dt.timedelta(days=365)
    precipitation=(
        session.query(Measurement.date,Measurement.prcp)
        .filter(Measurement.date>=prev_year)
        .all()
    )
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
#Create a station route
@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Station.station).all()
    stations=list(np.ravel(results))
    return jsonify(stations=stations)
#Create a monthly temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year=dt.date(2017,8,23) - dt.timedelta(days=365)
    results=(
        session.query(Measurement.tobs)
        .filter(Measurement.station=='USC00519281')
        .filter(Measurement.date>=prev_year)
        .all()
        )
    temps=list(np.ravel(results))
    return jsonify(temps=temps)
#Create statistics route, this one is a little diffrerent from the rest as it has start and end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None,end=None):
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    
    if not end:
        results=(
            session.query(*sel)#The asterisk in sel is used to indicate there will ne multiple results for the query
            .filter(Measurement.date>=start)
            .all()
            )
        temps=list(np.ravel(results))
        return jsonify(temps)
    results=(
        session.query(*sel)
        .filter(Measurement.date>= start)
        .filter(Measurement.date<= end)
        .all()
        )
    temps=list(np.ravel(results))
    return jsonify(temps)    
