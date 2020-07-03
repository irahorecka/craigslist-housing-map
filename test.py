import os
import sys
import pandas as pd
from data_utils import (
    clean_data,
    link_geotag_to_counties,
    join_counties_to_craigslist_pddf,
)
from plotting_utils import county_map, coord_map

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "Data")


def main():
    # arg = sys.argv[1]
    # x = clean_data(arg)
    # # y = x.drop(x.index[1000:])
    # # link_geotag_to_counties(x)  # comment out if up to date json is est.
    # a = join_counties_to_craigslist_pddf(x)
    # a.to_csv(os.path.join(DATA_PATH, 'filtered.csv'))
    coord_map()


if __name__ == "__main__":
    main()
