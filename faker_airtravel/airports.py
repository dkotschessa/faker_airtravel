

from faker.providers import BaseProvider
from random import choice, sample, randint
from .constants import airport_list, airlines


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
        # {'airport': 'Bradley International Airport',
        #  'iata': 'BDL',
        #  'icao': 'KBDL',
        #  'city': 'Windsor Locks',
        #  'state': 'Connecticut',
        #  'country': 'United States'}
        ap = choice(airport_list)
        return ap

        

    def airport_name(self):
        airport = self.airport_object()
        name = airport.get('airport')
        return name

    def airport_iata(self):
        airport = self.airport_object()
        iata = airport.get('iata')
        return iata

    def airport_icao(self):
        icao_list  = [airport['icao'] for airport in airport_list if not airport['icao'] == '']
        icao = choice(icao_list)
        return icao

    
    def airline(self):
        airline = choice(airlines)
        return airline

    def flight(self):
        origin, destination = sample(airport_list, k=2)
        airline = choice(airlines)
        stops = choice([1,2,3,'non-stop'])
        price = randint(200, 1000)
        flight_object = {'airline' : airline,
                'origin': origin,
                'destination' : destination,
                'stops' : stops,
                'price' : price
        }
        return flight_object

