import datetime
import os
import numpy as np
import pandas as pd
from scipy import stats

# i.e. craigslistHousingDashboard path
BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "Data")


def clean_data(rel_filepath=os.path.join(DATA_PATH, "bigfile_geo.csv")):
    import_data = read_csv(rel_filepath)
    # chain func together for a cleaning pipeline
    cleaning_funcs = (
        rm_craigslist_repost_duplicates,
        convert_price_to_int,
        convert_date_to_dttm,
        convert_area_to_int,
        select_apt_housing_only,
        filter_date_one_week_today,
        rm_none_bedrooms,
        set_price_per_area,
        rm_outliers_price_per_area,
    )
    for func in cleaning_funcs:
        import_data = func(import_data)

    import_data.to_csv(os.path.join(DATA_PATH, "test.csv"))
    return import_data


def read_csv(rel_filepath):
    """Read input CSV and trim illegal chars in column."""
    pd_csv = pd.read_csv(rel_filepath)
    pd_csv.columns = (
        pd_csv.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    return pd_csv


def rm_craigslist_repost_duplicates(craigslist_pddf):
    craigslist_pddf_repost_none = craigslist_pddf.loc[
        craigslist_pddf["repost_of_post_id"] == "None"
    ]
    craigslist_pddf_repost_not_none_unique = craigslist_pddf.loc[
        craigslist_pddf["repost_of_post_id"] != "None"
    ].drop_duplicates(subset="repost_of_post_id")

    return craigslist_pddf_repost_none.append(craigslist_pddf_repost_not_none_unique)


def convert_price_to_int(craigslist_pddf):
    craigslist_pddf.price = (
        craigslist_pddf.price.str.replace("$", "").replace(",", "").astype("int")
    )
    return craigslist_pddf


def convert_date_to_dttm(craigslist_pddf):
    craigslist_pddf.date_posted = pd.to_datetime(craigslist_pddf.date_posted)
    craigslist_pddf.time_posted = pd.to_datetime(
        craigslist_pddf.time_posted, format="%H:%M"
    )
    return craigslist_pddf


def convert_area_to_int(craigslist_pddf):
    craigslist_pddf = craigslist_pddf.loc[craigslist_pddf.area != "None"]
    craigslist_pddf.area = craigslist_pddf.area.str.replace("ft2", "").astype("int")
    return craigslist_pddf


def select_apt_housing_only(craigslist_pddf):
    return craigslist_pddf.loc[
        craigslist_pddf.housing_category == "apts & housing for rent"
    ]


def set_price_per_area(craigslist_pddf):
    craigslist_pddf["price_per_area"] = craigslist_pddf.price / craigslist_pddf.area
    return craigslist_pddf.loc[craigslist_pddf.price_per_area > 0.1]


def filter_date_one_week_today(craigslist_pddf):
    return craigslist_pddf[
        craigslist_pddf.date_posted > datetime.datetime.now() - pd.to_timedelta("7day")
    ]


def rm_none_bedrooms(craigslist_pddf):
    return craigslist_pddf.loc[craigslist_pddf.bedrooms != "None"]


def rm_outliers_price_per_area(df):
    return df[(np.abs(stats.zscore(df.price_per_area)) < 0.2)]
