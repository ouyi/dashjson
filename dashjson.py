#!/usr/bin/env python

import sys, logging, argparse, json, os.path
from datadog import initialize, api
from abc import ABCMeta, abstractmethod

def load_json(f):
    with open(f, 'r') as json_file:
        json_str = json_file.read()
        json_obj = json.loads(json_str)
        return json_obj

def dump_json(dash_json, f):
    with open(f, 'w') as json_file:
        json.dump(dash_json, json_file, indent=4)

def authenticate(cred_json):
    initialize(**cred_json)

class DashboardHandler(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def import_json(self, dash_json, update): pass
    @abstractmethod
    def export_json(self, dash_id): pass

class TimeboardHandler(DashboardHandler):
    def import_json(self, dash_json, update):
        timeboard_json = dash_json['dash']
        # required fields
        title, description, graphs = timeboard_json['title'], timeboard_json['description'], timeboard_json['graphs']
        # optional fields
        template_variables = timeboard_json.get('template_variables', [])
        if update:
            api.Timeboard.update(timeboard_json['id'], title=title, description=description, graphs=graphs, template_variables=template_variables)
        else:
            api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables)
    def export_json(self, dash_id):
        return api.Timeboard.get(dash_id)

class ScreenboardHandler(DashboardHandler):
    def import_json(self, dash_json, update):
        # required fields
        board_title, widgets = dash_json['board_title'], dash_json['widgets']
        # optional fields
        template_variables = dash_json.get('template_variables', [])
        if update:
           raise Exception('Update not supported for screenboards')
        else:
            api.Screenboard.create(board_title=board_title, widgets=widgets, template_variables=template_variables)
    def export_json(self, dash_id):
        return api.Screenboard.get(dash_id)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description=
    """
    A tool for exporting (or importing) Datadog dashboards to (or from) json files.

    Examples

    - Export to json
    # python dashjson.py -e my_timeboard.json -d 12345
    # python dashjson.py -e my_screenboard.json -d 12345 -t s

    - Import from json
    # python dashjson.py -i my_timeboard.json
    # python dashjson.py -i my_screenboard.json -t s -n

    - Example content of the credentials file (your keys can be found at https://app.datadoghq.com/account/settings#api)
    # cat ~/.dashjson.json
    {
        "api_key": "abcdefg12345678",
        "app_key": "abcdefg987654321"
    }
    """, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-c", "--credentials", default=os.path.join(os.path.expanduser('~'), '.dashjson.json'), help="the json file containing api_key and app_key as dictionary entries, defaults to ~/.dashjson.json")
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument("-i", "--import_file", help="the json file to import dashboard definition from")
    mutex_group.add_argument("-e", "--export_file", help="the json file to export dashboard definition to")
    parser.add_argument("-d", "--dash_id", type=int, help="the id of the dashboard to be exported")
    parser.add_argument("-t", "--dash_type", choices=['t', 's'], default='t', help="the type of the dashboard (t for timeboard and s for screenboard) to be imported or exported, default to t")
    parser.add_argument("-u", "--update", dest='update', action='store_true', help="update an existing timeboard (used in combination with -i, default for Timeboards, not supported for screenboards))")
    parser.add_argument("-n", "--no-update", dest='update', action='store_false', help="create a new dashboard (used in combination with -i)")
    parser.set_defaults(update=True)
    args = parser.parse_args()

    if args.export_file and not args.dash_id:
       parser.print_help()
       sys.exit(1)

    authenticate(load_json(args.credentials))

    handler = TimeboardHandler() if args.dash_type == 't' else ScreenboardHandler()

    if args.import_file:
        handler.import_json(load_json(args.import_file), args.update)
    elif args.export_file:
        dump_json(handler.export_json(args.dash_id), args.export_file)

if __name__ == "__main__":
    main()
