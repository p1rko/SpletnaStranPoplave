from flask import Flask, render_template, jsonify
from database import HydroStation, HydroMeasurement, MeteoStation, MeteoMeasurement, Prediction, session, engine
from sqlalchemy import select


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vizija")
def vizija():
    return render_template("vizija.html")

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")

@app.route("/api")
def api():
    return render_template("api_data.html")

@app.route("/model")
def model():
    return render_template("model.html")
@app.route("/zemljevid")
def zemljevid():
    return render_template("zemljevid1.html")



@app.route('/api/measurements/hydro')
def display_hydro_measurements():
    data = session.query(HydroMeasurement)
    return jsonify([i.serialize() for i in data.all()])

@app.route('/api/measurements/meteo')
def display_meteo_measurements():
    data = session.query(MeteoMeasurement)
    return jsonify([i.serialize() for i in data.all()])

@app.route('/api/stations/hydro')
def display_hydro_stations():
    data = session.query(HydroStation)
    return jsonify([i.serialize() for i in data.all()])

@app.route('/api/stations/meteo')
def display_meteo_stations():
    data = session.query(MeteoStation)
    return jsonify([i.serialize() for i in data.all()])

@app.route('/api/predicitons')
def display_predictions():
    data = session.query(Prediction)
    return jsonify([i.serialize() for i in data.all()])



if __name__=='__main__':
    app.run(debug=True, port=8000)
