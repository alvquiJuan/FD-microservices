import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import json
import fuzzy_motor as fm

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.fdarch


@app.route('/')
def index():


    return "Sorry index do nothing yet"


@app.route('/register', methods=['POST'])
def new():
    reg_item = request.get_json(force=True)
    response = db.fdarch.insert_one(reg_item)

    return response.inserted_id
@app.route('/register', methods=['GET'])
def list():
    _items = db.fdarch.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items)

@app.route('/motorStatus',methods=['POST'])
def getMotorStatus():
    #read the thermal data
    data = request.get_json(silent=True)
    #compute the difference between armature and ambient temperature
    my_motor=fm.Thermal_fuzzy_motor()
    status = my_motor.compute_status(data["thermaldata"]["tm"],data["thermaldata"]["ta"])
    #do something
    return "motor status: " + str(status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
