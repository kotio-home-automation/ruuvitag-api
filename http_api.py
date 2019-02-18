'''
HTTP API for providing ruuvitag sensor readings

Endpoint: http://0.0.0.0:5000/ruuvitag

Requires:
    bottle
    ruuvitag_sensor
'''
import sys, json
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

def read_data():
    allData = []
    for mac in configuredTags.keys():
        sensor = RuuviTag(mac)
        sensor.update()
        tagData = sensor.state
        tagData['name'] = configuredTags[mac]
        allData.append(tagData)
    return allData

@get('/ruuvitag')
@enable_cors
def ruuvitag_data():
    response.content_type = 'application/json; charset=UTF-8'
    return format_tags_data(read_data())

if __name__ == '__main__':
    if (len(sys.argv) > 2):
        print('Too many arguments!')
        sys.exit(0)

    # First argument is this python file itself
    if (len(sys.argv) < 2):
        print('Program needs a tag configuration file as parameter, e.g.: python http_api.py tags.json')
        sys.exit(0)

    configurationFile = sys.argv[1]
    configuredTags = load_tag_configuration(configurationFile)

    try:
        run(host='0.0.0.0', port=5000, debug=True)
    except:
        pass
    finally:
        print('Exiting...')
