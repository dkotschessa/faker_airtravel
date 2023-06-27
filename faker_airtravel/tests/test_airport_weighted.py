from collections import OrderedDict
from datetime import date, datetime, timedelta
from faker import Faker

from faker_airtravel import AirTravelProvider
from faker_airtravel.constants import airport_list as ap
from faker_airtravel.constants import airlines as al

fake = Faker()
fake.add_provider(AirTravelProvider)

airports=ap[:3]
airlines=al[:3]

def test_airport_name_weight():
    fake.flight_data_source(
        airport_list=airports,
        weight_airports=[0.5, 0.5, 0]
    )

    airport = fake.airport_name()
    assert airport == airports[0].get('name') or airport == airports[1].get('name')


def test_iata_weight():
    fake.flight_data_source(
        airport_list=airports,
        weight_airports=[0.5, 0.5, 0]
    )

    airport = fake.airport_iata()
    assert airport == airports[0].get('iata') or airport == airports[1].get('iata')


def test_icao_weight():
    fake.flight_data_source(
        airport_list=airports,
        weight_airports=[0.5, 0.5, 0]
    )

    airport = fake.airport_icao()
    assert airport == airports[0].get('icao') or airport == airports[1].get('icao')

def test_airline_weight():
    fake.flight_data_source(
        airlines=airlines,
        weight_airlines=[0.5, 0.5, 0]
    )

    airline = fake.airline()
    assert airline in airlines[:2]

def test_flight_weight():
    fake.flight_data_source(
        airport_list=airports,
        airlines=airlines,
        weight_airlines=[0.5, 0.5, 0],
        weight_airports=[0.5, 0.5, 0],
    )

    OD={
        "ABQ": OrderedDict([
                ("ADZ", 1)
        ]),
        "ADZ": OrderedDict([
            ("ABQ", 0.5),
            ("ACE", 0.5)
        ])
    }

    flight = fake.flight(OD=OD)


    assert flight.get("airline") in airlines[:2]
    assert flight.get("origin").get("iata") == airports[0].get('iata') or airports[1].get('iata')
    assert flight.get("destination").get("iata") in ["ADZ", "ABQ", "ACE"]
    assert (
        flight.get("origin").get("iata") == "ABQ" and flight.get("destination").get("iata") == "ADZ" or
        flight.get("origin").get("iata") == "ADZ" and (
            flight.get("destination").get("iata") == "ABQ" or
            flight.get("destination").get("iata") == "ACE"
        ) or
        flight.get("origin").get("iata") == "ACE"
    )

def test_flight_weight_times():
    fake.flight_data_source(
        airport_list=airports,
        airlines=airlines,
        weight_airlines=[0.5, 0.5, 0]
    )

    OD_times={
        "ABQ": {
            "ADZ": 6
        },
    }

    flight = fake.flight(OD_times=OD_times)

    dep_time = datetime.strptime(flight.get("departure_time"), '%H:%M').time()
    arr_time = datetime.strptime(flight.get("arrival_time"), '%H:%M').time()

    dep_time = datetime.combine(date.today(), dep_time)
    arr_time = datetime.combine(date.today(), arr_time)

    if (flight.get("origin").get("iata") == "ABQ" and flight.get("destination").get("iata") == "ADZ"):
        assert dep_time + timedelta(hours=6) == arr_time
