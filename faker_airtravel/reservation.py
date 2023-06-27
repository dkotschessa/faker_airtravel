from datetime import timedelta
from typing import Callable, Optional
from faker import Faker
from faker.providers import BaseProvider
from faker.typing import DateParseType

from .commons import DATE_FORMAT, create_dict_weights
from .constants import cabin_class

import string

_fake = Faker()

class AirReservationProvider(BaseProvider):
    """
    A Provider for travel related test data.

    >>> from faker import Faker
    >>> from faker_airtravel import ReservationProvider
    >>> fake = Faker()
    >>> fake.add_provider(ReservationProvider)
    """

    def record_locator(self) -> str:
        return _fake.bothify(
            text='#?#???',
            letters=string.ascii_uppercase
        )
    
    def number_pax(self, min: int=1, max: int=4, weights:list[float]=None) -> int:
        pax_list = list(range(min, max+1))

        if weights:
            pax_list = create_dict_weights(pax_list, weights)

        return _fake.random_element(
            elements = pax_list
        )
    
    def frequent_flyer(self, weights:list[float]=None) -> int:
        frq_list = [0, 1]

        if weights:
            frq_list = create_dict_weights(frq_list, weights)

        return _fake.random_element(
            elements = frq_list
        )
    
    def leg_number(self, min: int=1, max: int=4, weights:list[float]=None) -> int:
        leg_list = list(range(min, max+1))

        if weights:
            leg_list = create_dict_weights(leg_list, weights)

        return _fake.random_element(
            elements = leg_list
        )
    
    def cabin_class(
        self,
        cabin_class: list=cabin_class,
        weights: list[float]=None
    ):
        if weights:
            cabin_class = create_dict_weights(cabin_class, weights)

        return _fake.random_element(
            elements = cabin_class
        )
    
    def date_creation_reservation(
        self,
        start_date: DateParseType = "-30y",
        end_date: DateParseType = "now"
    ) -> str:
        reservation_datetime = _fake.date_between_dates(date_start=start_date, date_end=end_date)
        reservation_date = reservation_datetime.strftime(DATE_FORMAT)

        return reservation_date

    def ticket_price(self) -> float:
        price = _fake.random_number(digits=4)

        return price
    
    def reservation(
        self,
        min_max_pax: tuple[int, int] = (1, 4),
        min_max_leg: tuple[int, int] = (1, 4),
        start_date: DateParseType = "-30y",
        end_date: DateParseType = "now",
        weights: dict[str, list[float]] = None,
        price_function: Optional[Callable] = None,
        args_price_function: Optional[dict] = None
    ):
        number_pax_w = None
        frq_flr_w = None
        leg_num_w = None
        cabin_class_w = None

        if weights:
            # Unpack weights
            number_pax_w = weights.get("number_pax")
            frq_flr_w = weights.get("frq_flr")
            leg_num_w = weights.get("leg_number")
            cabin_class_w = weights.get("cabin_class")
            
        record_locator = self.record_locator()
        number_pax = self.number_pax(min=min_max_pax[0], max=min_max_pax[1], weights=number_pax_w)
        frq_flr = self.frequent_flyer(weights=frq_flr_w)
        leg_number = self.leg_number(min=min_max_leg[0], max=min_max_leg[1], weights=leg_num_w)
        cabin_class = self.cabin_class(weights=cabin_class_w)
        date_creation_reservation = self.date_creation_reservation(start_date=start_date, end_date=end_date)

        # end_date is the departure date
        date_return = _fake.date_between(start_date=end_date, end_date=timedelta(days=60))
        date_return = date_return.strftime(DATE_FORMAT)

        ticket_price = self.ticket_price()

        if price_function:
            ticket_price = price_function(
                record_locator=record_locator,
                number_pax=number_pax,
                frq_flr=frq_flr,
                leg_number=leg_number,
                cabin_class=cabin_class,
                date_creation_reservation=date_creation_reservation,
                date_return=date_return,
                args_flight=args_price_function
            )

        return {
            "record_locator": record_locator,
            "number_pax": number_pax,
            "frq_flr": frq_flr,
            "leg_number": leg_number,
            "cabin_class": cabin_class,
            "date_creation_reservation": date_creation_reservation,
            "date_return": date_return,
            "ticket_price": ticket_price
        }


