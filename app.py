from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from models import db, User, Card, Collection
import json, os

from main.main import main_bp
from auth.auth import auth_bp

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = "INSERTACTUALSECRETKEYHERE"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir}/tcg.db"
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

def seed_database():
    """Import card data from JSON into the SQL database."""
    try:
        with open("card_data.json", "r") as f:
            cards_data = json.load(f)

        for key, data in cards_data.items():
            # Check if card already exists to avoid duplicates
            exists = Card.query.filter_by(name=data["name"]).first()
            if not exists:
                new_card = Card(
                    name=data.get("name"),
                    level=data.get("level"),
                    race=data.get("race"),
                    type=data.get("type"),
                    desc=data.get("desc"),
                    # .get() handles missing power/toughness for Lands/Artifacts
                    attack=data.get("attack"),
                    defence=data.get("defence"),
                    class_id=data.get("class_id"),
                )
                db.session.add(new_card)

        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.session.rollback()

@app.route("/", methods = ['GET', 'POST'])
def index():
   return render_template("index.html")

@app.route("/get_card_details", methods=["POST"])
def get_card_details():
    data = request.json
    card_class = data.get("className")

    card = Card.query.filter_by(class_id=card_class).first()
    card_info = card.make_json() if card else None

    if card_info:
        return jsonify({"success": True, "card": card_info})
    return jsonify({"success": False, "error": "Card not found"}), 404

@app.route("/add_to_collection", methods=["POST"])
def add_to_collection():
    data = request.json
    #If you've implemented User Login system, Uncomment the first line, then comment out the second line.
    user_id = current_user.id
    card_name = data.get("card_name")

    user = User.query.get(user_id)
    card = Card.query.filter_by(name=card_name).first()

    if not user or not card:
        return jsonify({"success": False, "error": "User or card not found"}), 404

    # Check if the user already has this card in their collection
    existing_entry = Collection.query.filter_by(user_id=user_id, card_id=card.id).first()
    if existing_entry:
        existing_entry.quantity += 1
    else:
        new_entry = Collection(user_id=user_id, card_id=card.id)
        db.session.add(new_entry)

    db.session.commit()
    return jsonify({"success": True, "message": "Card added to collection"})

@app.route("/collection/<int:user_id>", methods=["GET"])
def view_collection(user_id):
    c = Collection.query.filter_by(user_id=user_id).all()
    return render_template("main/collection.html", collection = c)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, host="0.0.0.0")
