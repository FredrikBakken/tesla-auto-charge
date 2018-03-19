#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import DateField


class BasicAuth_NewUser_Form(FlaskForm):
    nuUsername = StringField("Username", validators=[DataRequired()])
    nuPassword = PasswordField("Password", validators=[DataRequired()])
    nuNewusername = StringField("New username", validators=[DataRequired()])

class BasicAuth_NewPass_Form(FlaskForm):
    npUsername = StringField("Username", validators=[DataRequired()])
    npPassword = PasswordField("Password", validators=[DataRequired()])
    npNewpassword = PasswordField("New password", validators=[DataRequired()])

class Location_Form(FlaskForm):
    locations = SelectField("Locations", choices=[('SE1', 'SE1'), ('SE2', 'SE2'), ('SE3', 'SE3'), ('SE4', 'SE4'), ('FI', 'FI'), ('DK1', 'DK1'), ('DK2', 'DK2'), ('Oslo', 'NO1: Oslo'), ('Kr.sand', 'NO2: Kr.sand'), ('Molde', 'NO3: Molde'), ('Tr.heim', 'NO3: Tr.heim'), ('Tromsø', 'NO4: Tromsø'), ('Bergen', 'NO5: Bergen'), ('EE', 'EE'), ('LV', 'LV'), ('LT', 'LT')])

class Vehicle_Auth_Form(FlaskForm):
    vaUsername = StringField("Username", validators=[DataRequired()])
    vaPassword = PasswordField("Password", validators=[DataRequired()])

class Vehicle_Location_Form(FlaskForm):
    latitude = StringField("Latitude", validators=[DataRequired()])
    longitude = StringField("Longitude", validators=[DataRequired()])

class Vehicle_Battery_Charge_To_Form(FlaskForm):
    toDate = DateField("Date", validators=[DataRequired()])
    toTimeHour = SelectField("Hour", choices=[('00', '00'), ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')])
    toTimeMinute = SelectField("Minute", choices=[('00', '00'), ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59')])
