from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def home():
    return render_template('login.html')

@frontend_bp.route('/login')
def login_page():
    return render_template('login.html')

@frontend_bp.route('/invoices')
def invoices_page():
    return render_template('invoices.html')
