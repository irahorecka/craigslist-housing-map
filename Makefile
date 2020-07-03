clear:
	rm -rf ./__pycache__ ./data_utils/__pycache__ ./plotting_utils/__pycache__ ./.ipynb_checkpoints

data:
	awk '(NR == 1) || (FNR > 1)' ./Data/cl_data/*.csv > ./Data/cl_data/all_geo.csv