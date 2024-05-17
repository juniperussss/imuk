
conda activate imuk


path_origin=/home/alex/code/imuk                      

python_path=/home/alex/miniforge3/envs/imuk/bin/python      # and this
 


path_output="${path_origin}/localtest"                 
export PYTHONPATH=$PYTHONPATH:${path_origin}


output_path=



$python_path "${path_origin}/products/stationmaps/stationmap_metpy.py" $path_origin $path_origin
echo "script finisched"