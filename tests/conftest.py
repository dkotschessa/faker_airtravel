# -*- coding: utf-8 -*-
import os
import pytest
import sys
import json

from faker import Faker
from src.airtravel.airport_dict import airports as ap
 
local_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(local_path, '..'))

from src.airtravel import AirTravelProvider

@pytest.fixture(scope='module')
def fake():
    fixture = Faker()
    fixture.add_provider(AirTravelProvider)
    return fixture

@pytest.fixture
def airports():
    return ap