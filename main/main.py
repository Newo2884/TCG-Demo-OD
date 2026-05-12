from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import *

main_bp = Blueprint("main", __name__, template_folder="templates")

@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("main/index.html")

@login_required
@main_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("main/profile.html", user=user)
