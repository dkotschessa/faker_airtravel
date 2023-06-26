from datetime import date, datetime, timedelta
from faker import Faker

from faker_airtravel import AirTripProvider
from faker_airtravel import AirTravelProvider
from faker_airtravel.constants import airport_list as ap
from faker_airtravel.constants import airlines as al
from faker_airtravel.constants import cabin_class as cc

airports=ap[:3]
airlines=al[:3]

fake = Faker()
fake.add_provider(AirTripProvider)
fake.add_provider(AirTravelProvider)

def test_trip():
    trip = fake.trip()

    assert len(trip) == 5
    assert len(trip[0].get("reservations")) > 0 and len(trip[0].get("reservations")) <= 150

def test_trip_with_params():
    # Flight
    OD_times={
        "ABQ": {
            "ADZ": 1
        },
    }

    flight_parameters = {
        "OD_times": OD_times
    }

    # Reservation
    def price_function(**args):
        return 5
    
    weights_reservation = {
        "number_pax": [1, 0, 0, 0, 0],
        "frq_flr": [1, 0],
        "leg_num": [0.5, 0.5, 0],
        "cabin_class": [0.5, 0.5, 0, 0]
    }

    reservations_parameters = {
        "min_max_pax": (2,5),
        "min_max_leg": (1,3),
        "start_date": "-30y",
        "price_function": price_function,
        "weights": weights_reservation
    }

    flights = fake.trip(
        flight_parameters=flight_parameters,
        reservations_parameters=reservations_parameters,
        airport_list=airports,
        airlines=airlines,
        weight_airlines=[0.5, 0.5, 0]
    )

    for flight in flights:
        dep_date = datetime.strptime(flight.get("departure_date"), "%Y-%m-%d")

        dep_time = datetime.strptime(flight.get("departure_time"), '%H:%M').time()
        arr_time = datetime.strptime(flight.get("arrival_time"), '%H:%M').time()

        dep_time = datetime.combine(date.today(), dep_time)
        arr_time = datetime.combine(date.today(), arr_time)

        assert flight.get("airline") in airlines
        assert flight.get("origin").get("iata") in [airport.get('iata') for airport in airports]

        if (flight.get("origin").get("iata") == "ABQ" and flight.get("destination").get("iata") == "ADZ"):
            assert dep_time + timedelta(hours=1) == arr_time

        for reservation in flight["reservations"]:
            res_date = datetime.strptime(reservation.get("date_creation_reservation"), "%Y-%m-%d")

            assert reservation.get("ticket_price") == 5
            assert reservation.get("number_pax") == 2
            assert reservation.get("frq_flr") == 0
            assert reservation.get("leg_number") in [1, 2, 3]
            assert reservation.get("cabin_class") in cc[:2]
            assert res_date <= dep_date