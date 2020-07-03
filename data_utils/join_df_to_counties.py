import json
import os
import numpy as np
import pandas as pd

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "Data")

def join_counties_to_craigslist_pddf(craigslist_pddf, filename="county_loc.json")):
    full_filepath = os.path.join(DATA_PATH, filename)
    county_list = load_counties(full_filepath)
    geotagged_df = craigslist_pddf.loc[craigslist_pddf.post_has_geotag != "None"]
    geotagged_df['county'] = np.array(county_list)
    return geotagged_df

def load_counties(json_path):
    with open(json_path) as json_file:
        json_loaded = json.load(json_file)

    return [get_county_from_json(_json) for _json in json_loaded]


def get_county_from_json(request_json):
    try:
        json_loaded = json.loads(request_json)
        politics = json_loaded[0].get('politics')
        county_json = [politics[i] for i in range(len(politics)) if politics[i].get("friendly_type") == 'county']
        county_code = str(county_json[0]['code'].replace('_', ''))  # return county code from geo content
        return county_code
    except (TypeError, IndexError, json.JSONDecodeError) as error:
        return str(error)

