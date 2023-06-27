from datetime import datetime
from typing import Optional
from faker import Faker
from faker.providers import BaseProvider
from faker_airtravel import AirReservationProvider, AirTravelProvider
from faker_airtravel.commons import DATE_FORMAT

_fake = Faker()
_fake.add_provider(AirReservationProvider)
_fake.add_provider(AirTravelProvider)


class AirTripProvider(BaseProvider):
    def trip(
        self,
        n_trip: int=5,
        max_reservation_flight: int=150,
        flight_parameters: Optional[dict]=None,
        reservations_parameters: dict={},
        airport_list: Optional[list[dict]]=None,
        airlines: Optional[list[str]]=None,
        weight_airports: Optional[list[float]]=None,
        weight_airlines: Optional[list[float]]=None
    ):
        
        _fake.flight_data_source(
            airport_list=airport_list,
            airlines=airlines,
            weight_airports=weight_airports,
            weight_airlines=weight_airlines
        )

        trips = []
        for _ in range(n_trip):
            # create a flight
            if flight_parameters:
                trip = _fake.flight(**flight_parameters)
            else:
                trip = _fake.flight()

            trips.append(
                trip
            )

            reservations = []
            n_reservation = _fake.random_int(
                min=1,
                max=max_reservation_flight
            )

            dep_date = datetime.strptime(trip.get("departure_date"), DATE_FORMAT)

            for _ in range(n_reservation):
                # create a reservation

                reservations_parameters["end_date"] = dep_date
                reservations_parameters["args_price_function"] = trip
                
                reservation =_fake.reservation(**reservations_parameters)


                reservations.append(
                    reservation
                )

            trips[-1]["reservations"] = reservations

    
        return trips 
                

