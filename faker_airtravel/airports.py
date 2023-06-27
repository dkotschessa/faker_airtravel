from random import randint
from datetime import timedelta
from typing import Optional, OrderedDict, Union
from collections import OrderedDict

from faker import Faker
from faker.providers import BaseProvider, date_time

from .constants import airlines, airport_list
from .commons import DATE_FORMAT, HOUR_FORMAT, create_dict_weights

_fake = Faker()
_fake.add_provider(date_time)

class Airport():
    def __init__(
        self,
        name=None,
        iata=None,
        icao=None,
        city=None,
        state=None,
        country=None,
        d=None
    ):

        if d:
            for key, value in d.items():
                setattr(self, key, value)
        else:
            self.name = name
            self.iata = iata
            self.icao = icao
            self.city = city
            self.state = state
            self.country = country

    def asdict(self):
        return {
            'name': self.name,
            'iata': self.iata,
            'icao': self.icao,
            'city': self.city,
            'state': self.state,
            'country': self.country
        }

class Airline():
    def __init__(self, name):
        self.name = name

class AirTravelProvider(BaseProvider):
    """
    A Provider for travel related test data.

    >>> from faker import Faker
    >>> from faker_airtravel import AirtravelProvider
    >>> fake = Faker()
    >>> fake.add_provider(AirtravelProvider)
    """

    def __init__(self, generator):
        super().__init__(generator)
        self.airlines = [Airline(airline) for airline in airlines]
        self.airport_list = [Airport(d=airport) for airport in airport_list]

    def flight_data_source(
        self,
        airlines: Optional[list[dict]] = None,
        airport_list: Optional[list[dict]] = None,
        weight_airlines: Optional[list[float]]=None,
        weight_airports: Optional[list[float]]=None
    ):
        """Set a personal data source, ignoring the predefined constants

            :sample: airlines=[{
                'name': 'Albuquerque International Airport',
                'iata': 'ABQ',
                'icao': 'KABQ',
                'city': 'Albuquerque',
                'state': 'New Mexico',
                'country': 'United States'
            }, {
                'name': 'Arrecife Airport',
                'iata': 'ACE',
                'icao': 'GCRR',
                'city': 'San Bartolomé',
                'state': 'Canary Islands',
                'country': 'Spain'
            }],
            weight_airlines=[0.5, 0.4]

        """

        if airlines:
            airlines = [Airline(airline) for airline in airlines]
        else:
            airlines = self.airlines

        if airport_list:
            airport_list = [Airport(d=airport) for airport in airport_list]
        else:
            airport_list = self.airport_list

        if weight_airlines:
            airlines = create_dict_weights(airlines, weight_airlines)

        if weight_airports:
            airport_list = create_dict_weights(self.airport_list, weight_airports)


        self.airlines = airlines
        self.airport_list = airport_list

    def airport_object(self, airports=None) -> dict:
        # Returns a random airport dict example:
        # {'name': 'Bradley International Airport',
        #  'iata': 'BDL',
        #  'icao': 'KBDL',
        #  'city': 'Windsor Locks',
        #  'state': 'Connecticut',
        #  'country': 'United States'}

        if airports:
            filtered_airports = filter(lambda airport: airport.iata in airports, self.airport_list)
        else:
            filtered_airports = self.airport_list
       
        ap = _fake.random_element(elements=filtered_airports)
        return ap

    def airport_name(self) -> str:
        airport = self.airport_object()
        name = airport.name
        return name

    def airport_iata(self) -> str:
        airport = self.airport_object()
        iata = airport.iata
        return iata

    def airport_icao(self) -> str:
        airports = self.airport_list

        if not isinstance(self.airport_list, OrderedDict):
            airports = filter(
                lambda airport: not airport.icao == "",
                airports
            )

        icao = _fake.random_element(
            elements=airports
        ).icao

        return icao

    def airline(self) -> str:
        airline = _fake.random_element(
            elements=self.airlines
        ).name

        return airline

    def flight(
        self,
        OD: Optional[dict[str, Union[list[str], OrderedDict[str, float]]]]=None,
        OD_times: Optional[dict[str, dict[str, float]]]=None,
        start_date="-30y",
        end_date="now"
    ) -> dict:
        """Create a random flight

            :sample: OD="ABQ": OrderedDict([
                            ("ADZ", 1)
                        ]),
                        "ADZ": OrderedDict([
                            ("ABQ", 0.5),
                            ("ACE", 0.5)
                        ])
        """
        
        # Origin Destination choice
        if OD:
            # Select randomly origin from OD
            origin = self.airport_object(list(OD.keys()))
            origin_iata = origin.iata
            origin_airport = OD.get(origin_iata)

            if origin_airport:
                # Randomly select from the possible destinations
                destination_iata = _fake.random_element(
                    elements=OD.get(origin_iata)
                )
            else:
                # Not in the OD, return random airport
                destination_iata = _fake.random_element(
                    elements=self.airport_list
                ).iata

            # Find the airport object
            if isinstance(self.airport_list, OrderedDict):
                # If we have weighted airport list
                destination = next(
                    airport for airport in self.airport_list.keys()
                    if airport.iata == destination_iata
                )
            else:
                destination = next(
                    airport for airport in self.airport_list
                    if airport.iata == destination_iata
                )
        else:
            # No OD matrix, so just take two random airports
            origin, destination = _fake.random_elements(
                elements=self.airport_list,
                unique=True,
                length=2
            )
        
        # Airline choice
        airline = self.airline()

        # Departure date choice
        departure_datetime = _fake.date_time_between(start_date, end_date)
        departure_date = departure_datetime.strftime(DATE_FORMAT)
        departure_time = HOUR_FORMAT.format(departure_datetime.hour, departure_datetime.minute)

        # Arrival date time
        duration = randint(-19, 19)

        if OD_times:
            # Take trip lenght from OD time matrix

            origin_times = OD_times.get(origin.iata)
            if origin_times:
                destination_time = origin_times.get(destination.iata)
                if destination_time:
                    duration = destination_time
            

        arrival_datetime = departure_datetime+timedelta(hours=duration)
        arrival_date = arrival_datetime.strftime(DATE_FORMAT)
        arrival_time = HOUR_FORMAT.format(arrival_datetime.hour, arrival_datetime.minute)

        flight_object = {
            "airline": airline,
            "origin": origin.asdict(),
            "destination": destination.asdict(),
            "departure_date": departure_date,
            "departure_time": departure_time,
            "arrival_date": arrival_date,
            "arrival_time": arrival_time
        }

        return flight_object