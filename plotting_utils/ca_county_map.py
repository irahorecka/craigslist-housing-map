import json
import os
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "Data")

scl = (
    [0, "rgb(150,0,90)"],
    [0.125, "rgb(0, 0, 200)"],
    [0.25, "rgb(0, 25, 255)"],
    [0.375, "rgb(0, 152, 255)"],
    [0.5, "rgb(44, 255, 150)"],
    [0.625, "rgb(151, 255, 0)"],
    [0.75, "rgb(255, 234, 0)"],
    [0.875, "rgb(255, 111, 0)"],
    [1, "rgb(255, 0, 0)"],
)

rev_scl = [
    (0, "rgb(255, 0, 0)"),
    (0.125, "rgb(255, 111, 0)"),
    (0.25, "rgb(255, 234, 0)"),
    (0.375, "rgb(151, 255, 0)"),
    (0.5, "rgb(44, 255, 150)"),
    (0.625, "rgb(0, 152, 255)"),
    (0.75, "rgb(0, 25, 255)"),
    (0.875, "rgb(0, 0, 200)"),
    (1, "rgb(150,0,90)"),
]


def county_map(csv_path=os.path.join(DATA_PATH, "filtered.csv")):
    with urlopen(
        "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    ) as response:
        counties = json.load(response)

    county_data = pd.read_csv(csv_path, converters={"county": lambda x: str(x)})
    county_data["price_per_area"] = county_data["price_per_area"].apply(
        lambda x: round(x, 2)
    )
    county_group = county_data.groupby(["county"]).median()
    county_group.reset_index(level=0, inplace=True)

    print(county_group)

    fig = px.choropleth_mapbox(
        county_group,
        geojson=counties,
        locations="county",
        color="price_per_area",
        color_continuous_scale=rev_scl,  # curl and Rainbow are good
        range_color=(
            county_group.price_per_area.min(),
            county_group.price_per_area.max(),
        ),
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 37.0902, "lon": -95.7129},
        opacity=0.5,
        labels={"unemp": "unemployment rate"},
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def coord_map(csv_path=os.path.join(DATA_PATH, "filtered.csv")):
    coord_data = pd.read_csv(csv_path)
    coord_data_truncated = coord_data.sample(n=10000, random_state=1)
    coord_data_truncated["price_per_area"] = coord_data_truncated[
        "price_per_area"
    ].apply(lambda x: round(x, 2))
    # coord_data_truncated = coord_data

    fig = go.Figure(
        data=go.Scattergeo(
            lat=coord_data_truncated["Lat"],
            lon=coord_data_truncated["Lon"],
            text="$" + coord_data_truncated["price_per_area"].astype(str) + " USD/SqFt",
            marker=dict(
                color=coord_data_truncated["price_per_area"],
                colorscale=scl,
                reversescale=True,
                opacity=0.7,
                size=4.0,
                colorbar=dict(
                    titleside="right",
                    outlinecolor="rgba(68, 68, 68, 0)",
                    ticks="outside",
                    showticksuffix="last",
                    dtick=0.1,
                ),
                cmax=4.8,
                cmin=coord_data_truncated.price_per_area.min(),
            ),
        )
    )

    fig.update_layout(
        geo=dict(
            scope="north america",
            showland=True,
            landcolor="rgb(212, 212, 212)",
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
            showsubunits=True,
            showcountries=True,
            resolution=50,
            projection=dict(type="conic conformal", rotation_lon=-100),
            lonaxis=dict(
                showgrid=True, gridwidth=0.5, range=[-124.7844079, -66.9513812], dtick=5
            ),
            lataxis=dict(
                showgrid=True, gridwidth=0.5, range=[24.7433195, 49.3457868], dtick=5
            ),
        ),
        title=f"Craigslist Apt/Housing posts (Jun 25, 2020 - July 2, 2020) :: USD per SqFt<br>N={coord_data_truncated.shape[0]}</a>",
    )
    fig.show()
