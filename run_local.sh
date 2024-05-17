#    . ~/.bashrc_miniconda3

#conda init
conda activate imuk

start=3
end=8
stepsize=3

path_origin=/home/alex/code/imuk                      
#python_path=/Users/alex/miniforge3/envs/imuk/bin/python   
#path_origin=/mnt/nvmente/CODE/imuk #/Users/alex/Code/imuk   # Change this 
python_path=/home/alex/miniforge3/envs/imuk/bin/python      # and this
 


path_output="${path_origin}/localtest"                 
export PYTHONPATH=$PYTHONPATH:${path_origin}
#path_input=/localdata/weathermaps/imuk


#path_output_klein=/localdata/weathermaps/webside/klein
#path_output_4panel=/localdata/weathermaps/webside/4panel
xdim_1=945
ydim_1=480


xdim_2=700
ydim_2=420


xdim_3=350
ydim_3=210

squaredimx=2751
squaredimy=2361

model1=icon
model2=icon-eu
model3=icon-d2

mode=summer

echo "request global started"

$python_path "${path_origin}/ressources/tools/request.py" $path_origin "${path_origin}/database/input/icon"
#echo "request global completed"

echo "request eu started"

#$python_path "${path_origin}/ressources/tools/request_eu.py" $path_origin "${path_origin}/database/input/icon-eu"
echo "request eu completed"

#$python_path "${path_origin}/ressources/tools/request_d2.py" $path_origin "${path_origin}/database/input/icon-d2"
#echo "request d2 completed"

#$python_path "${path_origin}/products/polarview/polarview.py" $xdim_1 $ydim_1 $path_output $path_origin $start $end $stepsize
#echo "850  finished"

#$python_path "${path_origin}/products/modell_weather/modell_weather.py"

#
#

echo $model1
#$python_path "${path_origin}/products/modell_weather/modell_wind.py"    $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model1
#$python_path "${path_origin}/products/modell_weather/modell_wind.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model2
#$python_path "${path_origin}/products/modell_weather/modell_wind.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model3



#$python_path "${path_origin}/products/modell_weather/modell_temp_2m.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model1
#$python_path "${path_origin}/products/modell_weather/modell_temp_2m.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model2
#$python_path "${path_origin}/products/modell_weather/modell_temp_2m.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model3


#
#$python_path "${path_origin}/products/modell_weather/modell_weather.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model1
#$python_path "${path_origin}/products/modell_weather/modell_weather.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model2
#$python_path "${path_origin}/products/modell_weather/modell_weather.py" $xdim_1 $xdim_1 $path_output $path_origin $start $end $stepsize $model3


#$python_path "${path_origin}/products/modell_weather/modell_cape_snow.py" $xdim_1 $xdim_1 $path_output $path_origin $start $ende $stepsize $model1 $mode
