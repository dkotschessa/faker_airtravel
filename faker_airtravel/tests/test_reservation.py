from faker import Faker

from faker_airtravel import AirReservationProvider
from faker_airtravel.constants import cabin_class as cc

fake = Faker()
fake.add_provider(AirReservationProvider)

def test_record_locator():
    name = fake.record_locator()
    assert len(name) == 6

def test_number_pax():
    number_pax = fake.number_pax(min=2, max=3)

    assert number_pax in [2, 3]

def test_frequent_flyer():
    frq_flr = fake.frequent_flyer()

    assert frq_flr in [0, 1]

def test_leg_number():
    leg_number = fake.leg_number(min=1, max = 3)

    assert leg_number in [1, 2, 3]

def test_cabin_class():
    cabin_class = fake.cabin_class()

    assert cabin_class in cc

def test_date_creation_reservation():
    date_creation_reservation = fake.date_creation_reservation()

    assert len(date_creation_reservation) == 10

def test_ticket_price():
    ticket_price = fake.ticket_price()

    assert isinstance(ticket_price, int) or isinstance(ticket_price, float)

def test_reservation():
    def price_function(**args):
        return 5

    reservation = fake.reservation(
        min_max_pax=(1,1),
        min_max_leg=(1,1),
        start_date="now",
        end_date="now",
        price_function=price_function
    )

    assert reservation.get("number_pax") == 1
    assert reservation.get("leg_number") == 1
    assert reservation.get("ticket_price") == 5