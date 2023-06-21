"""AirTravel Faker Community Provider"""

__version__ = "0.4"

from .airports import AirTravelProvider  # noqa: F401
from .reservation import AirReservationProvider
from .trip import AirTripProvider
