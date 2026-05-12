from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    mana_cost = db.Column(db.String(50))
    cmc = db.Column(db.Integer)
    type_line = db.Column(db.String(100))
    oracle_text = db.Column(db.Text)
    power = db.Column(db.String(10))
    toughness = db.Column(db.String(10))
    class_id = db.Column(db.String(50), unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)