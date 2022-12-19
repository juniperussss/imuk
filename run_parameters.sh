#request
/home/alex/miniforge3/envs/imuk/bin/python /home/alex/imuk/request.py /home/alex/imuk /home/alex/imuk/database/input/icon 


#Wind
#/opt/conda/bin/python /workspaces/imuk/wind_300.py 1920 1080 /workspaces/imuk/database/output/300 /workspaces/imuk
/home/alex/miniforge3/envs/imuk/bin/python /home/alex/imuk/wind_300.py 1920 1080 /home/alex/imuk/database/output/300 /home/alex/imuk
#relhum
#/opt/conda/bin/python /workspaces/imuk/gph_rh_700.py 1920 1080 /workspaces/imuk/database/output/700 /workspaces/imuk

/home/alex/miniforge3/envs/imuk/bin/python /home/alex/imuk/gph_rh_700.py 1920 1080 /home/alex/imuk/database/output/700 /home/alex/imuk

#Groundlevel
#/home/alex/miniforge3/envs/imuk/bin/python /home/alex/imuk/bd_sw_meteosat.py 1920 1080 /home/alex/imuk/database/output/1000_gl /home/alex/imuk

#Beta
/home/alex/miniforge3/envs/imuk/bin/python /home/alex/imuk/bd_sw_meteosat_beta.py 1920 1080 /home/alex/imuk/database/output/1000_gl /home/alex/imuk
