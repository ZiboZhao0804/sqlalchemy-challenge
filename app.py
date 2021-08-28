
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect = True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#Flask setup
app = Flask(__name__)

#Flask route

# 1. Home page - List all routes that are available.
@app.route("/")
def home():
    return(
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )

# 2. Convert the query results to a dictionary using date as the key and prcp as the value.
#    Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session=Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()
    session.close()
    #date and prcp list
    results_list = []
    for result in results:
        result_dict = {}
        result_dict['date'] = result.date
        result_dict['prcp'] = result.prcp
        results_list.append(result_dict)
    return jsonify(results_list)
    
# 3.Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session=Session(engine)
    results = session.query(Station.name).all()
    session.close()
    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))
    return jsonify(station_list)

# 4.Query the dates and temperature observations of the most active station for the last year of data.
#   Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session=Session(engine)
    # the most active station
    active_station = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()[0][0]
    # the most recent day
    recent_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).all()[0][0]
    # starting date
    starting_date = dt.datetime.strptime(recent_date,'%Y-%m-%d').date() - dt.timedelta(days = 365)
    # dates and temperature observations of the most active station for the last year of data
    results = session.query(Measurement.station,Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= starting_date).\
        filter(Measurement.station == active_station).all()
    session.close()
    # date and temp list
    results_list = []
    for result in results:
        result_dict = {}
        result_dict['station'] = result.station
        result_dict['date'] = result.date
        result_dict['temp'] = result.tobs
        results_list.append(result_dict)
    return jsonify(results_list)

# 5. Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end = 0):
     # Create our session (link) from Python to the DB
    session=Session(engine)
    # the most recent day
    recent_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).all()[0][0]
    if end == 0:
        # convert start and end date to datetime object
        end = dt.datetime.strptime(recent_date,'%Y-%m-%d').date()
    else:
        end = dt.datetime.strptime(end,'%Y-%m-%d').date()
    start = dt.datetime.strptime(start,'%Y-%m-%d').date()
    # check if the start and end input from user is within valid range
    start_date_in_data = session.query(Measurement.date).\
        order_by(Measurement.date).all()[0][0]
    start_date_in_data = dt.datetime.strptime(start_date_in_data,'%Y-%m-%d').date()
    end_date_in_data = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).all()[0][0]
    end_date_in_data = dt.datetime.strptime(end_date_in_data,'%Y-%m-%d').date()
    if start < start_date_in_data or end > end_date_in_data:
        return jsonify({"error": "User input date is out of valid range."}), 404
    #query
    tobs = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    query_temp = session.query(*tobs).\
        filter(func.strftime('%Y-%m-%d',Measurement.date) >= start).\
        filter(func.strftime('%Y-%m-%d',Measurement.date) <= end).all()
    min_temp = query_temp[0][0]
    max_temp = query_temp[0][1]
    avg_temp = round(query_temp[0][2],2)
    session.close()
    return (
        f'Summary temperature from {start} - {end}<br/>'
        f'minimum temperature: {min_temp}<br/>'
        f'maximum temperature: {max_temp}<br/>'
        f'average temperature: {avg_temp}'
    )
if __name__ == "__main__":
    app.run(debug = True)
