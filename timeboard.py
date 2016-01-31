#!/usr/bin/env python

import logging, argparse, json
from datadog import initialize, api

def loadjson(f):
    with open(f, 'r') as json_file:
        json_str = json_file.read()
        json_obj = json.loads(json_str)
        return json_obj

def authenticate(cred_json):
    initialize(**cred_json)

def import_json(timeboard_json):
    dash_json = timeboard_json['dash']
    title, description, graphs = dash_json['title'], dash_json['description'], dash_json['graphs']
    api.Timeboard.create(title=title, description=description, graphs=graphs)

def export_json(dash_id, f, t):
    dash_json = api.Timeboard.get(dash_id) if t == "t" else api.Screenboard.get(dash_id)
    if dash_json:
        with open(f, 'w') as json_file:
            json.dump(dash_json, json_file, indent=4)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description=
    """
    A tool for importing datadog dashboards from json files and exporting them to json files.
    """
    )
    parser.add_argument("-c", "--credentials", required=True, help="the json file containing api_key and app_key as dictionary entries")
    parser.add_argument("-i", "--import_file", help="the json file to import dashboard definition from")
    parser.add_argument("-e", "--export_file", help="the json file to export dashboard definition to")
    parser.add_argument("-d", "--dash_id", help="the id of the dashboard to be exported")
    parser.add_argument("-t", "--dash_type", help="the type (t or s) of the dashboard to be exported")
    args = parser.parse_args()

    authenticate(loadjson(args.credentials))

    if args.import_file:
        import_json(loadjson(args.import_file))
    elif args.export_file and args.dash_id:
        export_json(args.dash_id, args.export_file, args.dash_type)

if __name__ == "__main__":
    main()
