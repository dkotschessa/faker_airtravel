from faker import Faker

from faker_airtravel import AirReservationProvider
from faker_airtravel.constants import cabin_class as cc

fake = Faker()
fake.add_provider(AirReservationProvider)

def test_number_pax():
    number_pax = fake.number_pax(
        min=2,
        max=5,
        weights=[1, 0, 0, 0, 0]
    )

    assert number_pax == 2

def test_frequent_flyer():
    frq_flr = fake.frequent_flyer(
        weights=[1, 0]
    )

    assert frq_flr == 0

def test_leg_number():
    leg_number = fake.leg_number(
        min=1,
        max=3,
        weights=[0.5, 0.5, 0]
    )

    assert leg_number in [1, 2, 3]

def test_cabin_class():
    cabin_class = fake.cabin_class(
        weights = [0.5, 0.5, 0, 0]
    )

    assert cabin_class in cc[:2]

def test_reservation():
    def price_function(**args):
        return 5
    
    weights = {
        "number_pax": [1, 0, 0, 0, 0],
        "frq_flr": [1, 0],
        "leg_num": [0.5, 0.5, 0],
        "cabin_class": [0.5, 0.5, 0, 0]
    }

    reservation = fake.reservation(
        min_max_pax=(2,5),
        min_max_leg=(1,3),
        start_date="now",
        end_date="now",
        price_function=price_function,
        weights=weights
    )

    assert reservation.get("ticket_price") == 5
    assert reservation.get("number_pax") == 2
    assert reservation.get("frq_flr") == 0
    assert reservation.get("leg_number") in [1, 2, 3]
    assert reservation.get("cabin_class") in cc[:2]