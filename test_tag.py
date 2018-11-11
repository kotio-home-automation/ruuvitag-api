from unittest import TestCase
import json
from tag.tag import load_tag_configuration, format_tags_data

class TestTagConfigurationLoading(TestCase):

    def test_three_tags_are_defined(self):
        fileName = 'tag/tags.json'
        tagsConfiguration = load_tag_configuration(fileName)
        self.assertEqual(len(tagsConfiguration), 3)

    def test_non_existing_file_raises_error(self):
        fileName = 'not_existing.json'
        with self.assertRaises(FileNotFoundError):
            load_tag_configuration(fileName)


class TestTagFormatting(TestCase):

    def test_tag_data_is_formatted_properly(self):
        tagInputData = [{"pressure": 1021.83, "temperature": 23.43, "humidity": 36.0, "name": "Extra", "battery": 2530}]
        expectedTagOutput = [{"name": "Extra", "data": {"pressure": 1021.83, "humidity": 36.0, "temperature": 23.43}}]
        actualTagOutputData = json.loads(format_tags_data(tagInputData).decode('utf-8'))
        self.assertEqual(actualTagOutputData, expectedTagOutput)

    def test_formatting_incomplete_tag_data_raises_error(self):
        tagInputData = [{"temperature": 23.43, "humidity": 36.0, "name": "Extra", "battery": 2530}]
        with self.assertRaises(KeyError):
            format_tags_data(tagInputData)
