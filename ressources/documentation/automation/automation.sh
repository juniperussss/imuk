#!/bin/sh

~/miniforge3/bin/activate imuk && cd ~/imuk/ && ~/miniforge3/envs/imuk/bin/python request.py && ~/miniforge3/envs/imuk/bin/python bd_sw_meteosat.py ~/miniforge3/envs/imuk/bin/python gph_temp_850.py && ~/miniforge3/envs/imuk/bin/python gph_rh_700.py && ~/miniforge3/envs/imuk/bin/python gph_temp_500.py && ~/miniforge3/envs/imuk/bin/python wind_300.py