
# Airtravel provider for Faker


## Acknowlegements


`faker_airtravel` is a provider for the `Faker` Python package, and a fork of https://github.com/kennethwsmith/faker_vehicle.  I would like to thank the maintainer of that repository, since I used the structure to create this one.


## Description

`faker_airtravel` provides airtravel related fake data for testing purposes.  The definition of "fake" in this context really means "random," as the airport codes, cities, and locations are real.  However, I make no claims about accuracy, so do not use this as location data!


## Installation

Install with pip:

``` bash
pip install faker_airtravel

```

Add as a provider to your Faker instance:

``` python

from faker import Faker
from faker_airtravel import AirTravelProvider
fake.add_provider(AirTravelProvider)

```

If you already use faker, you probably know the conventional use is:

```python
fake = Faker()

```


### Airport Object

``` python
>>> fake.airport_object()
{'airport': 'Tocumen International Airport',
'iata': 'PTY',
'icao': 'MPTO',
'city': 'Tocumen',
'state': 'Panama',
'country': 'Panama'}

>>> fake.airport_name()
'Lisbon Airport'

```

### Airport Codes (IATA and ICAO)

``` python
>>> fake.airport_iata()
'LSC'

>>> fake.airport_icao()
'KOKC'
```

### Airlines
```
>>> fake.airline()
'Sichuan Airlines'

```

### Flight

The flight object is an example of how the data might be combined to create larger structures, and may not be the exact format you need.
However it does have the advantage that it will never choose the same 'origin' and 'destination' object.

```
>>>fake.flight()

{'airline': 'Maya Island Air',
 'origin': {'airport': 'Noi Bai Airport',
  'iata': 'HAN',
  'icao': 'VVNB',
  'city': 'Hanoi',
  'state': 'Ha Noi',
  'country': 'Vietnam'},
 'destination': {'airport': 'Geneva Airport',
  'iata': 'GVA',
  'icao': 'LSGG',
  'city': 'Geneva',
  'state': 'Canton of Geneva',
  'country': 'Switzerland'},
 'stops': 'non-stop',
 'price': 641}
 ```


 


