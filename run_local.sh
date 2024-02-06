#    . ~/.bashrc_miniconda3

#conda init
conda activate imuk

start=0
end=3 #168
stepsize=3

path_origin=/home/alex/CODE/imuk #/Users/alex/Code/imuk                           # Change this

python_path=/home/alex/miniforge3/envs/imuk/bin/python #/Users/alex/miniforge3/envs/imuk/bin/python     # and this
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

#$python_path "${path_origin}/ressources/tools/request.py" $path_origin "${path_origin}/database/input/icon"
#echo "data read"


$python_path "${path_origin}/products/polarview/polarview.py" $xdim_1 $ydim_1 $path_output $path_origin $start $end $stepsize
echo "850  finished"