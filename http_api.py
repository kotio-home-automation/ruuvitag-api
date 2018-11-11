'''
HTTP API for providing ruuvitag sensor readings

Endpoint: http://0.0.0.0:5000/ruuvitag

Requires:
    bottle
    ruuvitag_sensor
'''
from bottle import get, response, run
from ruuvitag_sensor.ruuvi_rx import RuuviTagReactive
from tag.tag import load_tag_configuration, format_tags_data

allData = {}

@get('/ruuvitag')
def ruuvitag_data():
    response.content_type = 'application/json; charset=UTF-8'
    return format_tags_data(allData.values())

if __name__ == '__main__':
    configuredTags = load_tag_configuration('tag/tags.json')

    def handle_new_data(data):
        global allData
        tagMacAddress = data[0]
        tagData = data[1]
        tagData['name'] = configuredTags[tagMacAddress]
        allData[tagMacAddress] = tagData

    ruuvi_rx = RuuviTagReactive(list(configuredTags.keys()))
    data_stream = ruuvi_rx.get_subject()
    data_stream.subscribe(handle_new_data)

    try:
        run(host='0.0.0.0', port=5000, debug=True)
    except:
        pass
    finally:
        ruuvi_rx.stop()
