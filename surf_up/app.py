import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the database
session = Session(engine)

# Flask setup
app = Flask(__name__)

# Flask routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation data
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).all()
    
    # Convert list of tuples into dictionary
    prcp_data_list = dict(prcp_data)

    return jsonify(prcp_data_list)

@app.route("/api/v1.0/stations")
def stations():
    # Query stations
    stations = session.query(Station.station).all()

    # Unravel results and convert to a list
    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query temperature observations of the most active station for the last year of data.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station == 'USC00519281').all()

    # Unravel results and convert to a list
    tobs_data_list = list(np.ravel(tobs_data))

    return jsonify(tobs_data_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    start_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Unravel results and convert to a list
    start_data_list = list(np.ravel(start_data))

    return jsonify(start_data_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    start_end_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Unravel results and convert to a list
    start_end_data_list = list(np.ravel(start_end_data))

    return jsonify(start_end_data_list)


if __name__ == '__main__':
    app.run(debug=True)
