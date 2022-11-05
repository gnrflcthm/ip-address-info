from flask import Blueprint, render_template, flash, request, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models import Ipinfo, User
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
    ipInfos = Ipinfo.query.all()
    return render_template("home.html", user=current_user, ipInfos=ipInfos)


@ views.route('/ip-info', methods=['GET', 'POST'])
@ login_required
def ip_info(address=None) -> Dict:
    IP_API_URL = "https://ipapi.co"
    address = session.get('customIPAddress', None)
    res = get(
        f'{IP_API_URL}/{address}/json') if address else get(f'{IP_API_URL}/json')
    if res.text == None:
        raise Exception("An Error has occured fetching IP Address Information")
    ipInfo = json.loads(res.text)
    ipInfo['languages'] = ipInfo['languages'].replace(",", ", ").upper()

    if request.method == 'POST':
        ip = ipInfo['ip']
        labelname = request.form.get('labelName')

        isIPExisting = Ipinfo.query.filter_by(ip=ip).first()

        if isIPExisting:
            flash('This IP Address had already been saved.', category='error')
            return redirect(url_for('views.home'))
        else:
            if labelname != "":
                newIp = Ipinfo(ip=ip, labelname=labelname)
                db.session.add(newIp)
                db.session.commit()
                flash('IP Address Information saved.', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Please input a label name for this IP Address.',
                      category='error')
                return redirect(url_for('views.ip_info'))

    return render_template("ipInfo.html", user=current_user, ipInfo=ipInfo)


@ views.route('/delete-ip', methods=['POST'])
def delete_ip():
    ip = json.loads(request.data)
    ipAddress = ip['ipAddress']
    ip = Ipinfo.query.get(ipAddress)
    if ip:
        db.session.delete(ip)
        db.session.commit()
    return jsonify({})


@ views.route('/accounts', methods=['GET', 'POST'])
@ login_required
def accounts():
    if current_user.id > 3:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        session['changePasswordFor'] = request.form.get('changePasswordFor')
        return redirect(url_for('auth.changePasswordFor'))

    users = User.query.all()
    return render_template("accounts.html", user=current_user, users=users)


@ views.route('/delete-acc', methods=['POST'])
def delete_acc():
    acc = json.loads(request.data)
    accID = acc['accID']
    acc = User.query.get(accID)
    if acc:
        db.session.delete(acc)
        db.session.commit()
    return jsonify({})
