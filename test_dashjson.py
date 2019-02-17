#!/usr/bin/env python

from unittest import TestCase
from unittest.mock import Mock
from dashjson import TimeboardHandler, ScreenboardHandler
import json, textwrap

class TestTimeboardHandler(TestCase):

    def setUp(self):
        self.api_mock = Mock()
        self.handler = TimeboardHandler(self.api_mock)

    def tearDown(self): pass

    def test_fromjson(self):
        timeboard_str = textwrap.dedent('''\
                {
                    "dash": {
                        "graphs": [
                            {
                                "definition": {
                                    "viz": "timeseries",
                                    "requests": [
                                        {
                                            "q": "avg:system.cpu.user{*}",
                                            "style": {
                                                "palette": "dog_classic",
                                                "width": "normal",
                                                "type": "solid"
                                            },
                                            "type": "line"
                                        }
                                    ]
                                },
                                "title": "Avg of system.cpu.user over *"
                            }
                        ],
                        "template_variables": [],
                        "description": "test timeboard description",
                        "title": "Test Timeboard Title",
                        "new_id": "xyz-5q5-abc",
                        "id": 4711
                    }
                }
                ''')

        dash_json = json.loads(timeboard_str)

        new_board = False
        self.handler.fromjson(dash_json, new_board)
        self.api_mock.update.assert_called_with(4711, title='Test Timeboard Title', description='test timeboard description', graphs=dash_json['dash']['graphs'], template_variables=[])

        new_board = True
        self.handler.fromjson(dash_json, new_board)
        self.api_mock.create.assert_called_with(title='Test Timeboard Title', description='test timeboard description', graphs=dash_json['dash']['graphs'], template_variables=[])

    def test_tojson(self):
        self.handler.tojson(4711)
        self.api_mock.get.assert_called_once_with(4711)

class TestScreenboardHandler(TestCase):

    def setUp(self):
        self.api_mock = Mock()
        self.handler = ScreenboardHandler(self.api_mock)

    def tearDown(self): pass

    def test_fromjson(self):
        screenboard_str = textwrap.dedent('''\
                {
                    "board_title": "Test Screenboard Title",
                    "description": "test screenboard description",
                    "widgets": [
                        {
                            "board_id": 4711,
                            "title_align": "left",
                            "title_size": 16,
                            "title": true,
                            "generated_title": "system.load.1",
                            "title_text": "",
                            "height": 13,
                            "tile_def": {
                                "viz": "query_value",
                                "requests": [
                                    {
                                        "q": "avg:system.load.1{*}",
                                        "aggregator": "avg",
                                        "style": {
                                            "width": "normal",
                                            "palette": "dog_classic",
                                            "type": "solid"
                                        },
                                        "type": null
                                    }
                                ]
                            }
                        }
                    ],
                    "id": 4711
                }
                ''')

        dash_json = json.loads(screenboard_str)

        new_board = False
        self.handler.fromjson(dash_json, new_board)
        self.api_mock.update.assert_called_with(4711, board_title='Test Screenboard Title', widgets=dash_json['widgets'], template_variables=[])

        new_board = True
        self.handler.fromjson(dash_json, new_board)
        self.api_mock.create.assert_called_with(board_title='Test Screenboard Title', widgets=dash_json['widgets'], template_variables=[])

    def test_tojson(self):
        self.handler.tojson(4711)
        self.api_mock.get.assert_called_once_with(4711)

if __name__ == '__main__':
    unittest.main()
