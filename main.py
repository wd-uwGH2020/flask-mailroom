import os
import base64
import peewee
from flask import Flask, render_template, request, redirect, url_for, session
from model import Donor, Donation 

app = Flask(__name__)
app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select().order_by(Donation.donor.asc(), Donation.value.desc())
    return render_template('donations.jinja2', donations=donations)

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            donor = Donor(name=request.form["name"])
            donor.save()
            return redirect(url_for("create_donation", donor_name=donor.name))
        except peewee.IntegrityError:
            return redirect(url_for("create_donation", donor_name=donor.name))
    else:
        return render_template('create.jinja2')   
@app.route('/create/<donor_name>', methods=["GET", "POST"])
def create_donation(donor_name):
    if request.method == "POST":
        donor = Donor.select().where(Donor.name==donor_name)
        donation = Donation(donor=donor, value=request.form["value"])
        donation.save()
        return redirect(url_for("all"))
    else:
        return render_template('create_donation.jinja2')   
   
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)

