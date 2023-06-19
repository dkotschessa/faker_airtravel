from random import choice, choices, randint, sample
from datetime import timedelta

from faker import Faker
from faker.providers import BaseProvider, date_time

from .constants import airlines, airport_list

_fake = Faker()
_fake.add_provider(date_time)

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
        self.airlines = airlines
        self.airport_list = airport_list

    def data_source(self, airlines, airport_list):
        self.airlines = airlines
        self.airport_list = airport_list

    def airport_object(self, weights:list[float]=None) -> dict:
        # Returns a random airport dict example:
        # {'airport': 'Bradley International Airport',
        #  'iata': 'BDL',
        #  'icao': 'KBDL',
        #  'city': 'Windsor Locks',
        #  'state': 'Connecticut',
        #  'country': 'United States'}
        ap = choices(
            population=self.airport_list,
            weights=weights
        )[0]
        return ap

    def airport_name(self, weights:list[float]=None) -> str:
        airport = self.airport_object(weights)
        name = airport.get("airport")
        return name

    def airport_iata(self, weights:list[float]=None) -> str:
        airport = self.airport_object(weights)
        iata = airport.get("iata")
        return iata

    def airport_icao(self, weights:list[float]=None) -> str:
        icao_list = [
            airport["icao"] for airport in airport_list if not airport["icao"] == ""
        ]

        icao = choices(
            population=icao_list,
            weights=weights
        )[0]

        return icao

    def airline(self, weights:list[float]=None) -> str:
        airline = choices(
            population = self.airlines,
            weights = weights
        )[0]

        return airline

    def flight(
        self,
        weight_airline:list[float]=None,
        weight_origin:dict[float]=None,
        OD: dict[str, list[str]]=None,
        OD_weight: dict[str, list[float]]=None,
        OD_times: dict[str, dict[str, float]]=None,
        start_date="-30y",
        end_date="now"
    ) -> dict:
        
        # Origin Destination choice
        if OD:
            # Select destination from OD
            origin = self.airport_object(weight_origin)
            origin_iata = origin.get("iata")

            destination_iata = choices(
                population=OD.get(origin_iata),
                weights=OD_weight.get(origin_iata)
            )[0]

            # Find the airport object
            destination = next(
                airport for airport in airport_list
                if airport.get("iata") == destination_iata
            )
        else:
            # No OD matrix, so just take two random airports
            origin, destination = sample(airport_list, k=2)
        
        # Airline choice
        airline = self.airline(weight_airline)

        # Departure date choice
        departure_datetime = _fake.date_time_between(start_date, end_date)
        departure_date = departure_datetime.strftime('%Y-%m-%d')
        departure_time = "{:d}:{:02d}".format(departure_datetime.hour, departure_datetime.minute)

        # Arrival date time
        if OD_times:
            duration = OD_times.get(origin_iata).get(destination_iata)
        else:
            duration = randint(-19, 19)

        arrival_datetime = departure_datetime+timedelta(hours=duration)
        arrival_date = arrival_datetime.strftime('%Y-%m-%d')
        arrival_time = "{:d}:{:02d}".format(arrival_datetime.hour, arrival_datetime.minute)

        flight_object = {
            "airline": airline,
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "departure_time": departure_time,
            "arrival_date": arrival_date,
            "arrival_time": arrival_time
        }

        return flight_object