
import random


import pytest
from faker import Faker

fake = Faker()
import src.airtravel
from src.airtravel import AirTravelProvider
from src.airtravel.airport_dict import airport_list as ap

fake.add_provider(AirTravelProvider)


@pytest.fixture
def airports():
    return ap

airport_keys = ['Airport', 'iata', 'icao', 'City', 'State', 'Country']

def test_airports(airports):
    assert len(airports) > 1

@pytest.mark.parametrize("test_input", airport_keys)
def test_dict_keys(airports, test_input):
    a = random.choice(airports)
    assert test_input in a.keys()

def test_airport_name():
    name = fake.airport_name()
    assert len(name) > 1

def test_iata():
    iata = fake.airport_iata()
    assert len(iata) >= 1

def test_icao():
    icao = fake.airport_icao() # not all airports have ICAO
    assert len(icao) >= 1



