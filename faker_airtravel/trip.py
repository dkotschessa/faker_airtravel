from datetime import datetime
from faker import Faker
from faker.providers import BaseProvider
from faker_airtravel import AirReservationProvider, AirTravelProvider

_fake = Faker()
_fake.add_provider(AirReservationProvider)
_fake.add_provider(AirTravelProvider)


class AirTripProvider(BaseProvider):
    def trip(
        self,
        n_trip: int=5,
        max_reservation_flight: int=150,
        flight_parameters: dict=None,
        reservations_parameters: dict={}
    ):

        trips = []
        for _ in range(n_trip):
            # create a flight
            if flight_parameters:
                trip =_fake.flight(**flight_parameters)
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

            dep_date = datetime.strptime(trip.get("departure_date"), "%Y-%m-%d")

            for _ in range(n_reservation):
                # create a reservation

                reservations_parameters["end_date"] = dep_date
                
                reservation =_fake.reservation(**reservations_parameters)


                reservations.append(
                    reservation
                )

            trips[-1]["reservations"] = reservations

    
        return trips 
                

