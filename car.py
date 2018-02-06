#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import library for starting car connection
import teslajson


# Connecting to car
def car_connection(username, password):
    connection = teslajson.Connection(username, password)
    return connection


# Find car location
def location(car):
    return True


# Start car charging
def start_charge(car):
    return True


# Stop car charging
def stop_charge(car):
    return True
