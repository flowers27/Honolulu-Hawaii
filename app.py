import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    max_date = max_date[0]

    year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    
    results_percipitation_dict = dict(results_percipitation)
    
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    
    results_station = session.query(Measurement.station).group_by(Measurement.station).all()

    stations_list = list(np.ravel(results_station))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = max_date[0]

    year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") = dt.timedelta(days=366)

    results_tobs = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    tobs_list = list(result_tobs)
    
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    between_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    between_dates = list(between_dates)
    return jsonify(between_dates_list)

if __name__ == '__main__':
    app.run(debug=True)