import os
import pandas as pd
from data_utils import clean_data, link_geotag_to_counties, join_counties_to_craigslist_pddf
from plotting_utils import make_plot

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "Data")

def main():
    x = clean_data()
    # y = x.drop(x.index[100:])
    # link_geotag_to_counties(x)
    a = join_counties_to_craigslist_pddf(x)
    a.to_csv(os.path.join(DATA_PATH, 'filtered.csv'))
    make_plot()


if __name__ == '__main__':
    main()