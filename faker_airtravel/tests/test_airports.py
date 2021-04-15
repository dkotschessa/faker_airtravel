import random

import pytest
from faker import Faker
from faker_airtravel import AirTravelProvider
from faker_airtravel.constants import airport_list as ap

fake = Faker()
fake.add_provider(AirTravelProvider)




@pytest.fixture
def airports():
    return ap

airport_keys = ['airport', 'iata', 'icao', 'city', 'state', 'country']

def test_airports(airports):
    assert len(airports) > 1

@pytest.mark.parametrize("test_input", airport_keys)
def test_dict_keys(airports, test_input):
    a = random.choice(airports)
    assert test_input in a.keys()

def test_airport_name():
    name = fake.airport_name()
    assert len(name) > 4

def test_iata():
    iata = fake.airport_iata()
    assert len(iata) == 3

def test_icao():
    icao = fake.airport_icao()
    assert len(icao) == 4

def test_airline():
    airline = fake.airline()
    assert len(airline) >= 1

def test_flight():
    flight = fake.flight()
    assert len(flight) == 5