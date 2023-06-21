# import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 
from datetime import datetime
from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# data_setup = datetime(Measurement.date)

# Flask Setup
#################################################
app = Flask(__name__)


# Query for the dates and temperature observations from the last year.

@app.route("/")
def home():
    return("/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
     "/api/v1.0/start<br/>"
     "/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    #first_dict = list(np.ravel(results1))
#  Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
   
    temps_dict = {}
    for date,prcp in results1:
        
        temps_dict[date] = prcp
     

#  Return the JSON representation of your dictionary.
    return jsonify(temps_dict)

# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station).all()

    sec_dict = list(np.ravel(results2))


# # #  Return the JSON representation of your dictionary.

    return jsonify(sec_dict)


# # * `/api/v1.0/tobs`
# #   * Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date>="2016-08-23").\
            filter(Measurement.date<="2017-08-23").\
    filter(Measurement.station=='USC00519281').all()

            
    #temp_dict = list(np.ravel(results3))
# # #  Convert the query results to a Dic

# #  Convert the query results to a Dictionary.
     
    temp_dict = {}
    for date, temps in results3:
        
        temp_dict[date] = temps
    
        #third_dict.append(temp_dict)

# #  Return the JSON representation of your dictionary.

    return jsonify(temp_dict)


# # * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

# #   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# #   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

# #   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


@app.route("/api/v1.0/<start>")
def start1(start):
    start_date = datetime.strptime(start, "%Y-%m-%d" )

    results4 = session.query( func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
            filter(Measurement.date>=start_date).all()
   

    
    temp_dates = list(np.ravel(results4))
   
# #  Return the JSON representation of your dictionary.

    return jsonify(temp_dates)
    # return jsonify(temp_dates)

@app.route("/api/v1.0/<start>/<end>")
def start2(start,end):
    start_date = datetime.strptime(start, "%Y-%m-%d" )
    end_date = datetime.strptime(end, "%Y-%m-%d" )
    results4 = session.query( func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
                filter(Measurement.date <= end_date).all()
   

    
    temp_dates = list(np.ravel(results4))
    # #  Convert the query results to a Dictionary.
  

    return jsonify(temp_dates)
    
if __name__ == '__main__':
    app.run(debug=True)
