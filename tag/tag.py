import json

class Tag:
    def __init__(self, tagData):
        self.name = tagData['name']
        self.data = {}
        self.data['pressure'] = tagData['pressure']
        self.data['humidity'] = tagData['humidity']
        self.data['temperature'] = tagData['temperature']

def load_tag_configuration(fileName):
    with open(fileName) as tagConfigurationFile:
        configuredTags = json.load(tagConfigurationFile)
    tagConfigurationFile.close()
    return configuredTags

def format_tags_data(completeTagsData):
    tagData = []
    for data in completeTagsData.values():
        tag = Tag(data)
        tagData.append(tag.__dict__)
    sortedTagData = sorted(tagData, key=lambda tag: tag['name'])
    return json.dumps(sortedTagData, ensure_ascii=False).encode('utf8')
