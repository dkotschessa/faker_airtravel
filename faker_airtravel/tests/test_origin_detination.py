from faker import Faker
from faker_airtravel import AirTravelProvider


fake = Faker()

def test_origin_destination_different():
    for provider in (AirTravelProvider, ):
        fake.add_provider(provider)

    for _ in range(10_000):
        random_flight = fake.flight()
        d_iata = random_flight["origin"]["iata"]
        a_iata = random_flight["destination"]["iata"]
        assert d_iata != a_iata