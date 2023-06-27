# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date, I put a random date (yyyy-mm-dd): /api/v1.0/2008-12-27<br/>"
        f"Temperature stat from start to end dates, I put a random date (yyyy-mm-dd): /api/v1.0/2006-08-27/2008-12-27<br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results from your precipitation analysis
    # (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.

    # Calculate the date one year ago from the latest date in the database
    session = Session(engine)
    latest_date = (
        session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    )
    latest_date = dt.datetime.strptime(latest_date, "%Y-%m-%d").date()
    one_year_ago = latest_date - relativedelta(months=12)

    # Query the precipitation data for the last 12 months
    sel = [Measurement.date, Measurement.prcp]
    queryresult = session.query(*sel).filter(Measurement.date >= one_year_ago).all()
    session.close()

    precipitation = []
    for date, prcp in queryresult:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    session = Session(engine)
    sel = [
        Station.station,
        Station.name,
        Station.latitude,
        Station.longitude,
        Station.elevation,
    ]
    queryresult = session.query(*sel).all()
    session.close()

    stations = []
    for station, name, lat, lon, el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    # Return a JSON list of temperature observations for the previous year.
    session = Session(engine)
    lateststr = (
        session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    )
    latestdate = dt.datetime.strptime(lateststr, "%Y-%m-%d")
    querydate = dt.date(latestdate.year - 1, latestdate.month, latestdate.day)
    sel = [Measurement.date, Measurement.tobs]
    queryresult = session.query(*sel).filter(Measurement.date >= querydate).all()
    session.close()

    tobsall = []
    for date, tobs in queryresult:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature
    for a specified start or start-end range."""
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal
    # to the start date.
    session = Session(engine)
    queryresult = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )
    session.close()

    tobsall = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature for a
    specified start-end range."""
    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start
    # date to the end date, inclusive.
    session = Session(engine)
    queryresult = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )
    session.close()

    tobsall = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
