import pytest
import src.airtravel    

def test_airports(fake, airports):
    assert len(airports) > 1

def test_dict_keys(airports):
    assert len(airports) > 1
    a = airports[0]
    assert 'Airport' in a.keys()
    assert 'iata' in a.keys()
    assert 'City' in a.keys()
    assert 'State' in a.keys()

def test_airport_name(fake, airports):
    name = fake.airport_name()
    assert len(name) > 1

def test_iata(fake, airports):
    iata = fake.airport_iata()
    assert len(iata) >= 1

