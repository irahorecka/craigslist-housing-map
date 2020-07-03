import json
import os
import time
import requests
from .concurrency import map_threads

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "Data")


def link_geotag_to_counties(craigslist_pddf):
    https_geocode = geocode_to_api_url(craigslist_pddf)
    response_gen = map_threads(get_request, https_geocode)
    response_list = list(response_gen)
    utf_responses = [req.decode("utf-8") for req in response_list]
    write_utf_response_to_json(utf_responses)


def geocode_to_api_url(craigslist_pddf):
    craigslist_pddf = craigslist_pddf.loc[craigslist_pddf.post_has_geotag != "None"]
    geo_tup = tuple(eval(loc) for loc in craigslist_pddf["post_has_geotag"])

    return tuple(
        f"http://www.datasciencetoolkit.org/coordinates2politics/{geo[0]}%2c{geo[1]}"
        for geo in geo_tup
    )


def get_request(geo_http):
    request = requests.get(geo_http)
    try:
        county_code = request.content
    except (TypeError, IndexError, json.JSONDecodeError) as error:  # NoneType, etc..
        county_code = error

    return county_code


def write_utf_response_to_json(response_list):
    with open(os.path.join(DATA_PATH, "county_loc.json"), 'w') as outfile:
        json.dump(response_list, outfile)


def get_ca_county(location):
    try:
        content = _input.decode("utf-8")
        politics = json.loads(content)[0]["politics"]
        #         print([politics[i] for i in range(len(politics)) if politics[i].get("friendly_type") == 'county'])
        _politics = []
        #         for i in range(len(politics)):
        #             # filter only california
        #             if politics[i].get("friendly_type") == "state":
        #                 if politics[i].get('name') == 'California':
        #                     pass
        #                 else:
        #                     return

        county_json = [
            politics[i]
            for i in range(len(politics))
            if politics[i].get("friendly_type") == "county"
        ]
        country_code = str(
            county_json[0]["code"].replace("_", "")
        )  # return county code from geo content
        return country_code
    except (TypeError, IndexError, json.JSONDecodeError) as error:  # Nonetype
        return str(error)
