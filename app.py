#by ELO
# 1. Import Flask
from flask import Flask, jsonify


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
        return f"API: /api/v1.0/precipitation"

@app.route("/api/v1.0/stations")
def station():
        return f"API: /api/v1.0/stations"

@app.route("/api/v1.0/tobs")
def tobs():
        return f"API: /api/v1.0/tobs"


if __name__ == "__main__":
    app.run(debug=True)
