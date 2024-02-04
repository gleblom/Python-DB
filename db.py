from flask import Flask, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3
from sqlalchemy import create_engine
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://5432:pass@localhost/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Machine(db.Model):
    __tablename__ = 'Machine'
    MachineID = db.Column(db.Integer, primary_key = True)
    Machine = db.Column(db.Text)


class Material(db.Model):
    __tablename = 'Material'
    MaterialID = db.Column(db.Integer, primary_key = True)
    Material = db.Column(db.Text)

class MachineMaterial(db.Model):
    __tablename__ = 'MachineMaterial'
    ID = db.Column(db.Integer, primary_key = True)
    MachineID = db.Column(db.Integer, db.ForeignKey('machine.MachineID'))
    MaterialID = db.Column(db.Integer, db.ForeignKey('material.MaterialID'))

@app.route('/')
@app.route('/Machine', methods = ['GET', 'POST'])
def Add_Machine():
    req1 = request.json.get("MachineID")
    req2 = request.json.get("Machine")
    if request.json.get('MachineID') is None or request.json.get('Machine') is None:
        print(req1, req2, 111111111111111)
    else:
        mch = Machine(Machine = req2)
        db.session.add(mch)
        db.session.commit()
        print(Machine.query.all())
    return make_response('ok', 200)


def Add_Material():
    req1 = request.json.get("MaterialID")
    req2 = request.json.get("Material")
    if request.json.get('MaterialID') is None or request.json.get('Material') is None:
            print(req1, req2, 111111111111111)
    else:
        mtl = Material(Material = req2)
        db.session.add(mtl)
        db.session.commit()
        print(Material.query.all())
    return make_response('ok', 200)


def Add_MachineMaterial():
    req1 = request.json.get("ID")
    req2 = request.json.get("MachineID")
    req3 = request.json.get("MaterialID")
    if request.json.get('MaterialID') is None or request.json.get('MachineID') is None or
    req1 = request.json.get("ID"):
        print(req1, req2, 111111111111111)
    else:
        mcmt = MachineMaterial(MachineMaterial = req2, req3)
        db.session.add(mcmt)
        db.session.commit()
        print(MachineMaterial.query.all())
    return make_response('ok', 200)

def Delete_Machine():
    req1 = request.json.get("MachineID")
    req2 = request.json.get("Machine")
    if request.json.get('MachineID') is None or request.json.get('Machine') is None:
        print(req1, req2, 111111111111111)
    else:
        mch = Machine(Machine = req2)
        db.session.delete(mch)
        db.session.commit()
        print(Machine.query.all())
    return make_response('ok', 200)


def Delete_Material():
    req1 = request.json.get("MaterialID")
    req2 = request.json.get("Material")
    if request.json.get('MaterialID') is None or request.json.get('Material') is None:
            print(req1, req2, 111111111111111)
    else:
        mtl = Material(Material = req2)
        db.session.delete(mtl)
        db.session.commit()
        print(Material.query.all())
    return make_response('ok', 200)


def Delete_MachineMaterial():
    req1 = request.json.get("ID")
    req2 = request.json.get("MachineID")
    req3 = request.json.get("MaterialID")
    if request.json.get('MaterialID') is None or request.json.get('MachineID') is None or
    req1 = request.json.get("ID"):
        print(req1, req2, 111111111111111)
    else:
        mcmt = MachineMaterial(MachineMaterial = req2, req3)
        db.session.delete(mcmt)
        db.session.commit()
        print(MachineMaterial.query.all())
    return make_response('ok', 200)

    
if __name__ == '__main__':
    app.run(host='192.168.0.114')

    
    
    
