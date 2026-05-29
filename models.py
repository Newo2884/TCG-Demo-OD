from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(50))
    race = db.Column(db.Integer)
    type = db.Column(db.String(100))
    desc = db.Column(db.Text)
    attack = db.Column(db.String(10))
    defence = db.Column(db.String(10))
    class_id = db.Column(db.String(50), unique=True)

    def make_json(self):
        data = {
                "name" : self.name,
                "level" : self.level,
                "race" : self.race,
                "type" : self.type,
                "desc" : self.desc,
                "attack" : self.attack,
                "defence" : self.defence
        }
        return data
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    user = db.relationship("User", backref="collections", lazy=True)
    card = db.relationship("Card", backref="collections", lazy=True)