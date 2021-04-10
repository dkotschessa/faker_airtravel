# -*- coding: utf-8 -*-
from faker.providers import BaseProvider
from random import choice
from .airport_dict import airports

class AirTravelProvider(BaseProvider):
    """
    A Provider for travel related test data.

    >>> from faker import Faker
    >>> from faker_airtravel import AirtravelProvider
    >>> fake = Faker()
    >>> fake.add_provider(AirtravelProvider)
    """

    def airport_object(self):
        # Returns a random airport dict example: {"Airport": "Philadelphia International Airport", "iatta" : "PHL",  "City": "Philadelphia", "State": "PA"}
        ap = choice(airports)
        return ap

    def airport_name(self):
        airport = self.airport_object()
        name = airport.get('Airport')
        return name

    def airport_iata(self):
        airport = self.airport_object()
        iata = airport.get('iata')
        return iata

