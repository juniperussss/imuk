. ~/.bashrc_miniconda3
conda activate imuk

start=0
end=168
stepsize=3
path_input=/localdata/weathermaps/imuk
path_output=/localdata/weathermaps/webside/klein

xdim_1=350
ydim_1=210

xdim_2=700
ydim_2=420

xdim_3=945
ydim_3=480

python /localdata/weathermaps/imuk/request_beta.py /localdata/weathermaps/imuk /localdata/weathermaps/imuk/database/input/icon
echo "data readed"

python /localdata/weathermaps/imuk/wind_300.py $xdim_1 $ydim_1 $path_output $path_input $start $end $stepsize
echo "300 small finished"
python /localdata/weathermaps/imuk/gph_temp_850.py $xdim_1 $ydim_1 $path_output $path_input $start $end $stepsize
echo "850 small finished"
python /localdata/weathermaps/imuk/gph_temp_500.py $xdim_1 $ydim_1 $path_output $path_input $start $end $stepsize
echo "500 small finished"
python /localdata/weathermaps/imuk/gph_rh_700.py $xdim_1 $ydim_1 $path_output $path_input $start $end $stepsize
echo "700 small finished"
python /localdata/weathermaps/imuk/bd_sw_meteosat_beta.py $xdim_1 $ydim_1 $path_output $path_input $start $end $stepsize
