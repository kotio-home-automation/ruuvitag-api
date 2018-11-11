import json

class Tag:
    def __init__(self, tagData):
        self.name = tagData['name']
        self.data = {}
        self.data['pressure'] = tagData['pressure']
        self.data['humidity'] = tagData['humidity']
        self.data['temperature'] = tagData['temperature']

def load_tag_configuration():
    with open('tags.json') as tagConfigurationFile:
        configuredTags = json.load(tagConfigurationFile)
    tagConfigurationFile.close()
    return configuredTags

def format_tags_data(fullTagDatas):
    tagData = []
    for data in fullTagDatas:
        tag = Tag(data)
        tagData.append(tag.__dict__)
    return json.dumps(tagData, ensure_ascii=False).encode('utf8')
