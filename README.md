# dashjson.py -- a Datadog tool

A tool for exporting (or importing) Datadog dashboards to (or from) json. It allows the Datadog dashboard definitions to be

- version controlled as json files, and
- migrated across Datadog accounts

<pre>
usage: dashjson.py [-h] [-c CREDENTIALS] (-i IMPORT_FILE | -e EXPORT_FILE)
                   [-d DASH_ID] [-t {t,s}] [-u] [-n]

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


optional arguments:
  -h, --help            show this help message and exit
  -c CREDENTIALS, --credentials CREDENTIALS
                        the json file containing api_key and app_key as dictionary entries, defaults to ~/.dashjson.json
  -i IMPORT_FILE, --import_file IMPORT_FILE
                        the json file to import dashboard definition from
  -e EXPORT_FILE, --export_file EXPORT_FILE
                        the json file to export dashboard definition to
  -d DASH_ID, --dash_id DASH_ID
                        the id of the dashboard to be exported
  -t {t,s}, --dash_type {t,s}
                        the type of the dashboard (t for timeboard and s for screenboard) to be imported or exported, default to t
  -u, --update          update an existing timeboard (used in combination with -i, default for Timeboards, not supported for screenboards))
  -n, --no-update       create a new dashboard (used in combination with -i)
</pre>
