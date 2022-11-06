import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)
@app.route("/")
#def welcome():
#    return

def welcome():
    return(
    '''
    <h1>Welcome to the Climate Analysis API!</h1>
    <h4>Available Routes:</h4>
    <ul>
        <li>/api/v1.0/precipitation</li>
        <li>/api/v1.0/stations</li>
        <li>/api/v1.0/tobs</li>
        <li>/api/v1.0/temp/start/end</li>
    </ul>
    ''')

@app.route('/api/v1.0/precipitation')
def precipitation():
    return {date:prcp for date, prcp in session.query(Measurement.date,Measurement.prcp).all()}

@app.route('/api/v1.0/stations')
def stations():
    return {id:location for id, location in session.query(Station.station,Station.name).all()}

@app.route('/api/v1.0/tobs')
def tobs():
    return {date:temperature for date, temperature in session.query(Measurement.date,Measurement.tobs).all()}

@app.route('/api/v1.0/<start>/')
@app.route('/api/v1.0/<start>/<end>')
def tempRange(start, end = '2017-08-23'):
    temp = Measurement.tobs
    data = session.query(func.min(temp),func.max(temp),func.avg(temp)).filter((Measurement.date>=start)&(Measurement.date<=end)).all()

    return jsonify(dict(data))


if __name__ == "__main__":
    app.run()
