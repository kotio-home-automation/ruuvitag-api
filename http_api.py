'''
HTTP API for providing ruuvitag sensor readings

Endpoint: http://0.0.0.0:5000/ruuvitag

Requires:
    bottle
    ruuvitag_sensor
'''
import sys, json, time, threading, datetime
from bottle import get, response, request, run
from ruuvitag_sensor.ruuvitag import RuuviTag
from tag.tag import load_tag_configuration, format_tags_data

# borrowed from https://ongspxm.github.io/blog/2017/02/bottlepy-cors/
def enable_cors(func):
    def wrapper(*args, **kwargs):
        response.set_header("Access-Control-Allow-Origin", "*")
        response.set_header("Content-Type", "application/json")
        response.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Content-Type")

        # skip the function if it is not needed
        if request.method == 'OPTIONS':
            return

        return func(*args, **kwargs)
    return wrapper

configuredTags = dict()
cachedData = []
nextRun = time.time()

def read_data():
    global cachedData
    allData = []
    for mac in configuredTags.keys():
        sensor = RuuviTag(mac)
        sensor.update()
        tagData = sensor.state
        tagData['name'] = configuredTags[mac]
        allData.append(tagData)
    cachedData.clear()
    return allData

def cache_data():
    print('[{}] Refreshing cache'.format(datetime.datetime.now()))
    global cachedData
    global cacheTimer
    global nextRun
    cachePeriodSeconds = 30
    cachedData = read_data()
    nextRun = nextRun + cachePeriodSeconds
    intervalInSeconds = nextRun - time.time()
    cacheTimer = threading.Timer(intervalInSeconds, cache_data)
    cacheTimer.start()

cacheTimer = threading.Timer(0, cache_data)

@get('/ruuvitag')
@enable_cors
def ruuvitag_data():
    response.content_type = 'application/json; charset=UTF-8'
    return format_tags_data(cachedData)

if __name__ == '__main__':
    # First argument is this python file itself
    if (len(sys.argv) < 2):
        print('Program needs a tag configuration file as parameter, e.g.: python http_api.py tags.json')
        sys.exit(0)

    global configuredTags
    configurationFile = sys.argv[1]
    configuredTags = load_tag_configuration(configurationFile)
    cacheTimer.start()

    try:
        run(host='0.0.0.0', port=5000, debug=True)
    except:
        pass
    finally:
        print('Exiting...')
        cacheTimer.cancel()

