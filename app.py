import time
import schedule

from flask import Flask, flash, render_template, redirect, request, url_for
from flask_basicauth import BasicAuth

from backend import scheduler
from spot_values import get_spot_values
from database import select_location_elspot
from config import set_secret_key, get_basic_authentication

from forms import BasicAuthenticationForm


### Flask application setup
app = Flask(__name__)

### Application configuration
app.config['SECRET_KEY'] = set_secret_key()

basic_authentication = get_basic_authentication()
app.config['BASIC_AUTH_USERNAME'] = basic_authentication[0]
app.config['BASIC_AUTH_PASSWORD'] = basic_authentication[1]

### Functionality
basic_auth = BasicAuth(app)


# ROUTE: Index/Home
@app.route('/')
def index():
    return render_template('home.html')


# ROUTE: About
@app.route('/about')
def about():
    return render_template('about.html')


# ROUTE: Elspot
@app.route('/elspot')
def elspot():
    elspot_data = select_location_elspot('Tr.heim')
    spot_location = elspot_data[0]
    spot_date = elspot_data[1]
    values = elspot_data[2]
    spot_prices = elspot_data[3]
    return render_template('elspot.html', values=values, spot_date = spot_date, spot_location = spot_location, spot_prices = spot_prices)


# ROUTE: Settings
@app.route('/settings', methods=['GET', 'POST'])
@basic_auth.required
def settings():
    error = None
    basic_authentication_form = BasicAuthenticationForm()

    if request.method == 'POST':
        if not (request.form['username'] == get_basic_authentication()[0] and request.form['password'] == get_basic_authentication()[1]):
            error = 'Invalid credentials'

        else:
            new_password = request.form['newpassword']
            flash('You were successfully logged in')
            return redirect(url_for('settings'))
    return render_template('settings.html', error=error, basic_authentication_form = basic_authentication_form)


if __name__ == "__main__":
    scheduler()

    # Flask application
    app.run(debug=True, host='192.168.1.76', port=5050, use_reloader=False)
