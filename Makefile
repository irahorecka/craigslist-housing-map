clean:
	rm -rf ./__pycache__ ./data_utils/__pycache__ ./plotting_utils/__pycache__ ./.ipynb_checkpoints

black:
	black ./test.py ./data_utils/clean_raw_data.py ./data_utils/concurrency.py ./data_utils/county_id_from_geotag.py ./data_utils/join_df_to_counties.py ./plotting_utils/ca_county_map.py

dat:
	awk '(NR == 1) || (FNR > 1)' ./Data/cl_data/*.csv > ./Data/all_geo.csv
