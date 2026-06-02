from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import *

main_bp = Blueprint("main", __name__, url_prefix="/main", template_folder="templates")

@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@main_bp.route("/add_to_collection", methods=["POST"])
def add_to_collection():
    data = request.json
    user_id = current_user.id
    card_name = data.get("name")

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

@main_bp.route("/collection/<int:user_id>", methods=["GET"])
def view_collection(user_id):
    c = Collection.query.filter_by(user_id=user_id).all()
    return render_template("collection.html", collection = c)
