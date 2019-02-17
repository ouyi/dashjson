#!/usr/bin/env python

import sys, logging, argparse, json, os.path, textwrap
from datadog import initialize as dd_init, api as dd_api
from abc import ABCMeta, abstractmethod

def load_json(f):
    with open(f, 'r') as json_file:
        json_str = json_file.read()
        json_obj = json.loads(json_str)
        return json_obj

def dump_json(dash_json, f):
    with open(f, 'w') as json_file:
        json.dump(dash_json, json_file, indent=4)

class DashboardHandler(object):
    __metaclass__ = ABCMeta

    def __init__(self, api):
        self.api = api

    @abstractmethod
    def fromjson(self, dash_json, new_board): pass

    def tojson(self, board_id):
        return self.api.get(board_id)

class TimeboardHandler(DashboardHandler):

    def fromjson(self, dash_json, new_board):
        timeboard_json = dash_json['dash']
        # required fields
        title, description, graphs = timeboard_json['title'], timeboard_json['description'], timeboard_json['graphs']
        # optional fields
        template_variables = timeboard_json.get('template_variables')
        template_variables = template_variables if template_variables else []
        if new_board:
            self.api.create(title=title, description=description, graphs=graphs, template_variables=template_variables)
        else:
            self.api.update(timeboard_json['id'], title=title, description=description, graphs=graphs, template_variables=template_variables)

class ScreenboardHandler(DashboardHandler):

    def fromjson(self, dash_json, new_board):
        # required fields
        board_title, widgets = dash_json['board_title'], dash_json['widgets']
        # optional fields
        template_variables = dash_json.get('template_variables')
        template_variables = template_variables if template_variables else []
        if new_board:
            self.api.create(board_title=board_title, widgets=widgets, template_variables=template_variables)
        else:
            self.api.update(dash_json['id'], board_title=board_title, widgets=widgets, template_variables=template_variables)

def create_handler(cred_file, board_type):
    cred = load_json(cred_file)
    dd_init(**cred)
    return TimeboardHandler(dd_api.Timeboard) if board_type == 't' else ScreenboardHandler(dd_api.Screenboard)

def fromjson(args):
    create_handler(args.credentials, args.board_type).fromjson(load_json(args.json_file), args.new_board)

def tojson(args):
    dump_json(create_handler(args.credentials, args.board_type).tojson(args.board_id), args.json_file)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description=textwrap.dedent('''\
            A tool for exporting (or importing) Datadog dashboards to (or from) json files.

            Examples:

            - Export to json (the id can be found in the dashboard URL, normally numeric or alphanumeric)
            # python dashjson.py tojson -b xyz-123-abc my_timeboard.json
            # python dashjson.py -t s tojson -b 584086 my_screenboard.json

            - Import from json
            # python dashjson.py fromjson my_timeboard.json
            # python dashjson.py -t s fromjson my_screenboard.json

            - Import from json creating new dashboard
            # python dashjson.py fromjson -n my_timeboard.json
            # python dashjson.py -t s fromjson -n my_screenboard.json

            - Example content of the credentials file (your keys can be found at https://app.datadoghq.com/account/settings#api)
            # cat ~/.dashjson.json
            {
                "api_key": "abcdefg12345678",
                "app_key": "abcdefg987654321"
            }
            '''), formatter_class=argparse.RawTextHelpFormatter, allow_abbrev=True)
    parser.add_argument("-c", "--credentials", default=os.path.join(os.path.expanduser('~'), ".dashjson.json"), help="the json file containing api_key and app_key as dictionary entries, defaults to ~/.dashjson.json")
    parser.add_argument("-t", "--board-type", choices=['t', 's'], default='t', help="the type of the dashboard (t for timeboard and s for screenboard) to be imported or exported, default to t")

    subparsers = parser.add_subparsers(title="subcommands", description="run `python dashjson.py <subcommand> -h` for usage on a subcommand", help="valid subcommands")

    subparser_tojson = subparsers.add_parser("tojson", help="export a dashboard to a json file")
    subparser_tojson.add_argument("-b", "--board-id", help="the id of the dashboard to be exported")
    subparser_tojson.add_argument("json_file", help="the json file to be written to")
    subparser_tojson.set_defaults(func=tojson)

    subparser_fromjson = subparsers.add_parser("fromjson", help="import a dashboard from a json file")
    subparser_fromjson.add_argument("-n", "--new-board", action='store_true', help="create a new dashboard, without updating the existing one specified in the json file)")
    subparser_fromjson.add_argument("json_file", help="the json file to be read from")
    subparser_fromjson.set_defaults(func=fromjson)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
