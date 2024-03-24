import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)


class Animal(db.Model):
    __tablename__ = 'Animal'
    id = db.Column(db.Integer, primary_key=True)
    genus = db.Column(db.String(120))
    species = db.Column(db.String(120))
    specimens = db.relationship('Specimen', backref='animal', lazy=True)

class Institution(db.Model):
    __tablename__ = 'Institution'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(120))
    specimens = db.relationship('Specimen', backref='institution', lazy=True)

class Specimen(db.Model):
    __tablename__ = 'Specimen'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer,db.ForeignKey('Animal.id')
                          ,nullable=False)
    institution_id = db.Column(db.Integer,db.ForeignKey('Institution.id')
                          ,nullable=False)
    sightingdate = db.Column(db.DateTime)

# TODO update schema




