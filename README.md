# ruuvitag-api

HTTP REST JSON API for reading ruuvitag sensor data, implemented in Python.

## Prequisites

* Python 3.5 or later
* pip

Python 3.5+ is required because the application uses reactive extensions (rx) implementation of ruuvitag reader.

### Install dependencies

`pip install -r requirements.txt` or if you have pip for python 2 and 3 then `pip3 install -r requirements.txt`.

The `ruuvitag_sensor` module has a bunch of it's own requirements that need to be attended, see details from [ruuvitag-sensor's README](https://github.com/ttu/ruuvitag-sensor).

## Configuring application

The application needs to be configured so that it knows what ruuvitag beacons it subscribes to i.e. reads data from.
The configuration file is a JSON file and can be found at `tag/tags.json`, it contains a example configuration. The configuration consists of a
MAC address of the beacon and a descriptive name that will work as a identifier, the name can be chosen freely and be what ever seems appropriate e,g, a room name.

### Example configuration

```
{
  "CF:8C:D8:71:DC:BF": "Työhuone",
  "DC:AD:51:64:DC:27": "Makuuhuone"
}
```

## Run application

Once prequisites are met and dependencies installed the application can run as root `python http_api.py` or as sudo `sudo python http_api.py`. If you have
python 2 and 3 installed the command `python` probably needs to be replaced with command `python3`.

The application needs to run root or sudo because `ruuvitag_sensor` uses Bluez and that requires root privileges.

## Endpoint

http://0.0.0.0:5000/ruuvitag

## Response example

```
[
  {
    "data": {
      "pressure": 1021.29, "temperature": 23.31, "humidity": 36.5
    },
    "name": "Makuuhuone"
  },
  {
    "data": {
      "pressure": 1021.83, "temperature": 23.43, "humidity": 36.0
    },
    "name": "Työhuone"
  }
]
```

