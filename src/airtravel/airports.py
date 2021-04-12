

from faker.providers import BaseProvider
from random import choice
from .airport_dict import airport_list


class AirTravelProvider(BaseProvider):
    """
    A Provider for travel related test data.

    >>> from faker import Faker
    >>> from faker_airtravel import AirtravelProvider
    >>> fake = Faker()
    >>> fake.add_provider(AirtravelProvider)
    """

    def airport_object(self):
        # Returns a random airport dict example: 
        # {'Airport': 'Bradley International Airport',
        #  'iata': 'BDL',
        #  'icao': 'KBDL',
        #  'City': 'Windsor Locks',
        #  'State': 'Connecticut',
        #  'Country': 'United States'}
        ap = choice(airport_list)
        return ap

        

    def airport_name(self):
        airport = self.airport_object()
        name = airport.get('Airport')
        return name

    def airport_iata(self):
        airport = self.airport_object()
        iata = airport.get('iata')
        return iata

    def airport_icao(self):
        icao_list  = [airport['icao'] for airport in airport_list if not airport['icao'] == '']
        icao = choice(icao_list)
        return icao

    def airport_flight(self):
        airports = choices(airports, k=2)
        origin = airports[0]
        airport = self.airport_object()
        origin = airports
