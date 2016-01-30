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

def create(timeboard_json):
    dash_json = timeboard_json['dash']
    title, description, graphs = dash_json['title'], dash_json['description'], dash_json['graphs']
    api.Timeboard.create(title=title, description=description, graphs=graphs)

def export(dash_id, f):
    dash_json = api.Timeboard.get(dash_id)
    if dash_json:
        with open(f, 'w') as json_file:
            json.dump(dash_json, json_file, indent=4)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description=
    """
    A tool for creating datadog timeboards from json files and exporting them to json files.
    """
    )
    parser.add_argument("-c", "--credentials", required=True, help="json file containing api_key and app_key as dictionary entries")
    parser.add_argument("-f", "--fromjson", help="input json file containing the timeboard definition")
    parser.add_argument("-t", "--tojson", help="output json file containing the timeboard definition")
    parser.add_argument("-d", "--dash_id", help="id of the dashboard to be exported")
    args = parser.parse_args()

    authenticate(loadjson(args.credentials))

    if args.fromjson:
        create(loadjson(args.fromjson))
    elif args.tojson and args.dash_id:
        export(args.dash_id, args.tojson)

if __name__ == "__main__":
    main()
