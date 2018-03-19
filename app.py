#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
import charger
import backend
import logging
import schedule

from flask import Flask, flash, render_template, redirect, request, url_for
from flask_basicauth import BasicAuth

from datetime import datetime

from backend import scheduler
from spot_values import get_spot_values
from database import select_location_elspot
from config import set_secret_key, check_authentication, get_basic_authentication, set_new_authentication_username, set_new_authentication_password, check_location, get_current_elspot_location, set_new_elspot_location, check_vehicle, set_vehicle_home_location, get_charge_schedule, set_charge_to
from vehicle import register_credentials, vehicle_location

from forms import BasicAuth_NewUser_Form, BasicAuth_NewPass_Form, Location_Form, Vehicle_Auth_Form, Vehicle_Location_Form, Vehicle_Battery_Charge_To_Form


### Flask application setup
app = Flask(__name__)

### Application configuration
app.config['SECRET_KEY'] = set_secret_key()

basic_authentication = get_basic_authentication()
app.config['BASIC_AUTH_USERNAME'] = basic_authentication[0]
app.config['BASIC_AUTH_PASSWORD'] = basic_authentication[1]

### Functionality
basic_auth = BasicAuth(app)

### Setup of logging functionality
logging.basicConfig(filename="execution.log", level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


# ROUTE: Index/Home
@app.route('/')
def index():
    return render_template('home.html')


# ROUTE: Future charge
@app.route('/future')
def future():
    add_page = backend.charge_test
    #set_location = check_location()
    #set_vehicle = check_vehicle()
    home_location = get_current_elspot_location()

    mt = ''
    bl = ''
    cc = ''
    cv = ''
    cp = ''
    tfc = ''
    spot_dates = ''

    cs = get_charge_schedule()
    charge_schedule = sorted(cs, key=lambda x : (x['date'], x['hour']))

    if not add_page:
        mt = charger.measure_time
        bl = charger.battery_level
        cc = charger.charger_current
        cv = charger.charger_voltage
        cp = ((float(cc) * float(cv)) / 1000)
        tfc = str(math.floor(charger.time_to_full_charge)) + 'h ' + str(math.ceil((charger.time_to_full_charge - math.floor(charger.time_to_full_charge)) * 60)) + 'min'

        home_location   = get_current_elspot_location()
        elspot_data     = select_location_elspot(home_location)
        spot_dates      = elspot_data[1]

    return render_template('future.html', add_page=add_page, home_location=home_location, mt=mt, bl=bl, cp=cp, cc=cc, cv=cv, tfc=tfc, spot_dates=spot_dates, charge_schedule=charge_schedule)


# ROUTE: Previous charges
@app.route('/previous')
def previous():
    return render_template('previous.html')


# ROUTE: Previous | Date
@app.route('/previous/<date>')
def previous_date(date):
    return render_template('previous_data.html', date=date)


# ROUTE: Elspot
@app.route('/elspot')
def elspot():
    not_defined = 'False'
    home_location   = get_current_elspot_location()
    
    if home_location == '':
        home_location = 'SE1'
        not_defined = 'True'
    
    elspot_data     = select_location_elspot(home_location)
    spot_location   = elspot_data[0]
    spot_dates      = elspot_data[1]
    labels          = elspot_data[2]
    values          = elspot_data[3]
    spot_prices     = elspot_data[4]

    return render_template('elspot.html', home_location=home_location, labels=labels, values=values, spot_dates = spot_dates, spot_location = spot_location, spot_prices = spot_prices, not_defined=not_defined)


# ROUTE: Elspot | Other locations
@app.route('/elspot/<custom_location>')
def elspot_custom(custom_location):
    home_location   = get_current_elspot_location()
    elspot_data     = select_location_elspot(custom_location)
    spot_location   = elspot_data[0]
    spot_dates      = elspot_data[1]
    labels          = elspot_data[2]
    values          = elspot_data[3]
    spot_prices     = elspot_data[4]
    return render_template('elspot.html', home_location=home_location, labels=labels, values=values, spot_dates = spot_dates, spot_location = spot_location, spot_prices = spot_prices)


# ROUTE: About TAC
@app.route('/about')
def about():
    return render_template('about.html')


# ROUTE: Settings
@app.route('/settings', methods=['GET', 'POST'])
@basic_auth.required
def settings():
    error = None

    # Feedback to user
    set_auth = check_authentication()
    set_location = check_location()
    set_vehicle = check_vehicle()
    
    # Get vehicle location
    ve_location = vehicle_location()
    ve_lat = ve_location[0]
    ve_lng = ve_location[1]
    ve_zoom = ve_location[2]
    add_marker = ve_location[3]

    # Initialize forms
    basicAuth_NewUserForm     = BasicAuth_NewUser_Form()
    basicAuth_NewPassForm     = BasicAuth_NewPass_Form()
    location_Form             = Location_Form()
    current_location          = get_current_elspot_location()
    vehicleAuth_Form          = Vehicle_Auth_Form()
    vehicleLocation_Form      = Vehicle_Location_Form()
    vehicleBatteryCharge_Form = Vehicle_Battery_Charge_To_Form()

    # Change basic authentication username
    if basicAuth_NewUserForm.validate_on_submit():
        if not (request.form['nuUsername'] == get_basic_authentication()[0] and request.form['nuPassword'] == get_basic_authentication()[1]):
            error = 'Invalid credentials (username)'
        else:
            new_username = request.form['nuNewusername']
            set_new_authentication_username(app, new_username)
            flash('Your username has been changed!')
            return redirect(url_for('settings'))

    # Change basic authentication password
    if basicAuth_NewPassForm.validate_on_submit():
        if not (request.form['npUsername'] == get_basic_authentication()[0] and request.form['npPassword'] == get_basic_authentication()[1]):
            error = 'Invalid credentials'
        else:
            new_password = request.form['npNewpassword']
            set_new_authentication_password(app, new_password)
            flash('Your password has been changed!')
            return redirect(url_for('settings'))
    
    # Change elspot location
    if location_Form.validate_on_submit():
        new_location = request.form['locations']
        set_new_elspot_location(new_location)
        backend.charge_test = True
        flash('New home location has been set to ' + new_location + '!')
        return redirect(url_for('settings'))
    
    # Set vehicle authentication
    if vehicleAuth_Form.validate_on_submit():
        connection = register_credentials(request.form['vaUsername'], request.form['vaPassword'])

        if not connection:
            error = 'Invalid credentials (vehicle)'
        else:
            flash('Your vehicle credentials has been updated!')
            return redirect(url_for('settings'))
    
    # Set vehicle charge home location
    if vehicleLocation_Form.validate_on_submit():
        lat = request.form['latitude']
        lng = request.form['longitude']
        set_vehicle_home_location(lat, lng)
        flash('New vehicle home location has been set to lat: ' + lat + ', lng: ' + lng + '!')
        return redirect(url_for('settings'))

    # Set vehicle battery charge time to
    if vehicleBatteryCharge_Form.validate_on_submit():
        to_date = request.form['toDate']
        to_hour = request.form['toTimeHour']
        to_minute = request.form['toTimeMinute']

        # Formatting date and time
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        to_date = to_date.strftime("%Y.%m.%d")
        to_time = to_hour + ':' + to_minute

        # Insert time and date into config.json
        set_charge_to(to_date, to_time)

        backend.charge_test = True

        flash('Charge settings has been updated. Date: ' + to_date + ', time: ' + to_time + '.')
        return redirect(url_for('settings'))

    return render_template('settings.html', error=error, basicAuth_NewUserForm = basicAuth_NewUserForm, basicAuth_NewPassForm = basicAuth_NewPassForm, current_location = current_location, location_Form = location_Form, vehicleAuth_Form = vehicleAuth_Form, vehicleLocation_Form=vehicleLocation_Form, vehicleBatteryCharge_Form=vehicleBatteryCharge_Form, ve_lat=ve_lat, ve_lng=ve_lng, ve_zoom=ve_zoom, add_marker=add_marker, set_auth=set_auth, set_location=set_location, set_vehicle=set_vehicle)


if __name__ == "__main__":
    scheduler()

    # Flask application
    app.run(debug=True, host='0.0.0.0', port=5050, use_reloader=False)
