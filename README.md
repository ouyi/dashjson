# datadog tool dashjson.py

A tool for exporting (or importing) datadog dashboards to (or from) json

<pre>
usage: dashjson.py [-h] [-c CREDENTIALS] (-i IMPORT_FILE | -e EXPORT_FILE)
                   [-d DASH_ID] [-t {t,s}] [-u] [-n]

    A tool for exporting (or importing) datadog dashboards to (or from) json files.

    Examples

    - Export to json
    # python dashjson.py -e mydashboard.json -d 12345

    - Import from json
    # python dashjson.py -i mydashboard.json

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
                        the type of the dashboard (t for timeboard and s for screenboard) to be imported or exported
  -u, --update          update an existing timeboard (used in combination with -i, not supported for screenboards))
  -n, --no-update       create a new dashboard (used in combination with -i)
</pre>
