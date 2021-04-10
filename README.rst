# NOTE
# This is the very first iteration from a fork, and in no condition to be used or forked!



faker_vehicle
=============


faker_airtravel is a provider for the `Faker` Python package, and a fork of https://github.com/fcurella/faker_vehicle.  I thank the maintainer of this provider for it's existence, as this is nearly identical in structure.

It provides vehicle related fake data for testing purposes:

This will provide travel related "fake" data for testing purposes.  (i.e. the data is fake, but the airport codes/names are real). 

    * Airlines
    * Airports
    * Airport Locations
    * Airport Codes (IATA)
    
Future improvements may include

    * ICAO airport codes
    * Flights with prices
    
 


Usage
-----

Install with pip:

.. code:: bash

    pip install faker_travel

Or install with setup.py

.. code:: bash

    git clone https://github.com/dkotschessa/faker_airtravel.git
    cd faker_airtravel && python setup.py install

Add the ``AirTravelProvider`` to your ``Faker`` instance:

.. code:: python

    from faker import Faker
    from faker_vehicle import VehicleProvider

    fake = Faker()
    fake.add_provider(AirTravelProvider)
    fake.airline()
    # Delta Airlines
    fake.airport()
    # Philadelphia International Airport, Philadelphia, PA
    fake.airport_name()
    # Philadelphia International Airport
    fake.airport_iata()
    # PHL
   
   
    json.dumps(fake.airport_object())
    # {"Airport": Philadelphia International, "iata" : "PHL", "City" : "Philadelphia",  "State" : "PA"}
