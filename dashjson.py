#!/usr/bin/env python

import logging, argparse, json
from datadog import initialize, api

def load_json(f):
    with open(f, 'r') as json_file:
        json_str = json_file.read()
        json_obj = json.loads(json_str)
        return json_obj

def authenticate(cred_json):
    initialize(**cred_json)

def import_json(dash_json, t, update):
    if t == "t":
        timeboard_json = dash_json['dash']
        title, description, graphs = timeboard_json['title'], timeboard_json['description'], timeboard_json['graphs']
        if update:
            api.Timeboard.update(timeboard_json['id'], title=title, description=description, graphs=graphs)
        else:
            api.Timeboard.create(title=title, description=description, graphs=graphs)
    else:
        board_title, description, widgets = dash_json['board_title'], dash_json['description'], dash_json['widgets']
        if update:
           raise Exception('Update not supported for screenboards')
        else:
            api.Screenboard.create(board_title=board_title, description=description, widgets=widgets)

def export_json(dash_id, f, t):
    dash_json = api.Timeboard.get(dash_id) if t == "t" else api.Screenboard.get(dash_id)
    if dash_json:
        with open(f, 'w') as json_file:
            json.dump(dash_json, json_file, indent=4)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description=
    """
    A tool for exporting (or importing) datadog dashboards to (or from) json files.
    """
    )
    parser.add_argument("-c", "--credentials", required=True, help="the json file containing api_key and app_key as dictionary entries")
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument("-i", "--import_file", help="the json file to import dashboard definition from")
    mutex_group.add_argument("-e", "--export_file", help="the json file to export dashboard definition to")
    parser.add_argument("-d", "--dash_id", help="the id of the dashboard to be exported")
    parser.add_argument("-t", "--dash_type", choices=['t', 's'], default='t', help="the type of the dashboard to be imported or exported")
    parser.add_argument("-u", "--update", default=True, help="update an existing timeboard (used in combination with -i, not supported for screenboards")
    args = parser.parse_args()

    if args.export_file and not args.dash_id:
       parser.print_help()
       sys.exit(1)

    authenticate(load_json(args.credentials))

    if args.import_file:
        import_json(load_json(args.import_file), args.dash_type, args.update)
    elif args.export_file and args.dash_id:
        export_json(args.dash_id, args.export_file, args.dash_type)

if __name__ == "__main__":
    main()
