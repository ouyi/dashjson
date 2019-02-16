#!/usr/bin/env python

from unittest import TestCase
from unittest.mock import Mock
from dashjson import TimeboardHandler
import json, textwrap

class TestTimeboardHandler(TestCase):

    def test_import_json(self):
        api_mock = Mock()
        board = TimeboardHandler(api_mock)
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
            }''')

        dash_json = json.loads(timeboard_str)

        update = True
        board.import_json(dash_json, update)
        api_mock.update.assert_called_with(4711, title='Test Timeboard Title', description='test timeboard description', graphs=dash_json['dash']['graphs'], template_variables=[])

        update = False
        board.import_json(dash_json, update)
        api_mock.create.assert_called_with(title='Test Timeboard Title', description='test timeboard description', graphs=dash_json['dash']['graphs'], template_variables=[])
