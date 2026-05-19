from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User, Card, Collection
import json, os

from main.main import main_bp
from auth.auth import auth_bp

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "INSERTACTUALSECRETKEYHERE"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "tcg.db")
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
                    mana_cost=data.get("mana_cost"),
                    cmc=data.get("cmc"),
                    type_line=data.get("type_line"),
                    oracle_text=data.get("oracle_text"),
                    # .get() handles missing power/toughness for Lands/Artifacts
                    power=data.get("power"),
                    toughness=data.get("toughness"),
                    class_id=data.get("class_id"),
                )
                db.session.add(new_card)

        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.session.rollback()

@app.route("/")
def index():
   return render_template("main/index.html")

@app.route("/get_card_details", methods=["POST"])
def get_card_details():
    data = request.json
    card_class = data.get("className")

    card = Card.query.filter_by(class_id=card_class).first()
    card_info = card.make_json() if card else None

    if card_info:
        return jsonify({"success": True, "card": card_info})
    return jsonify({"success": False, "error": "Card not found"}), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, host="0.0.0.0")
