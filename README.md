usage: dashjson.py [-h] -c CREDENTIALS (-i IMPORT_FILE | -e EXPORT_FILE)
                   [-d DASH_ID] [-t {t,s}]

A tool for exporting (or importing) datadog dashboards to (or from) json
files.

optional arguments:
  -h, --help            show this help message and exit
  -c CREDENTIALS, --credentials CREDENTIALS
                        the json file containing api_key and app_key as
                        dictionary entries
  -i IMPORT_FILE, --import_file IMPORT_FILE
                        the json file to import dashboard definition from
  -e EXPORT_FILE, --export_file EXPORT_FILE
                        the json file to export dashboard definition to
  -d DASH_ID, --dash_id DASH_ID
                        the id of the dashboard to be exported
  -t {t,s}, --dash_type {t,s}
                        the type of the dashboard to be imported or exported
