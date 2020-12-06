#by ELO
# 1. Import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

engine = create_engine("sqlite://<Your Path Here>/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.datetime.strptime(end_date, "%Y-%m-%d") - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    session.close()

    prcp_dict = {}
    all_data = []
    for date, prcp in results:
            prcp_dict["date"] = date
            prcp_dict["prcp"] = prcp
            all_data.append(prcp_dict)

    return jsonify(all_data)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    results = session.query(Station.id, Station.station, Station.name).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():     
    session = Session(engine)
    end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.datetime.strptime(end_date, "%Y-%m-%d") - dt.timedelta(days = 365)
    station_active = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    Most_actv_st_id = station_active[0][0]
    temp = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == Most_actv_st_id, Measurement.date >= start_date).all()
    session.close()

    all_tobs = []
    tobs_dict = {}
    for tobs in temp:
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


if __name__ == "__main__":
    app.run(debug=True)
