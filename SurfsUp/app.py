# Import the dependencies.
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of precipitation data for the last 12 months."""
    # Perform the query to retrieve the precipitation data
    # Convert the query results to a dictionary using date as the key and prcp as the value
    # Return the JSON representation of the dictionary


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Perform the query to retrieve the list of stations
    # Return the JSON representation of the list of stations


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year of the most-active station."""
    # Perform the query to retrieve the temperature observations for the previous year of the most-active station
    # Return the JSON representation of the temperature observations


@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature for a specified start date."""
    # Perform the query to calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    # Return the JSON representation of the result


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature for a specified start-end range."""
    # Perform the query to calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive
    # Return the JSON representation of the result


# Run the app
if __name__ == "__main__":
    app.run(debug=True)


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB
