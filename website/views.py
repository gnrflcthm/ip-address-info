from argparse import Action
from flask import Blueprint, render_template, flash, request, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json

from typing import Dict  # For specifying a Dict return type in functions
from requests import get  # For http requests


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('customIPAddress') != "":
            session['customIPAddress'] = request.form.get('customIPAddress')
            return redirect(url_for('views.ip_info'))
        else:
            flash('Please input a valid public IP address.', category='error')
            pass
    #ipInfos = Ipinfo.query.all()
    return render_template("home.html", user=current_user)
