# -*- coding: utf-8 -*-
import re
import pytest
import src.airtravel

def test_airports(airports):
    assert len(airports) > 1

def test_dict_keys(airports):
    assert len(airports) > 1
    a = vehicles[0]
    assert 'Airport' in v.keys()
    assert 'iata' in v.keys()
    assert 'City' in v.keys()
    assert 'State' in v.keys()

def test_airport(airports):
    make = fake.airport()
    assert len(make) > 1

def test_airport_name(airports):
    name = fake.airport_name()
    assert len(name) > 1

def test_iata(airports):
    iata = fake.airport_iata()
    assert len(iata) >= 1

