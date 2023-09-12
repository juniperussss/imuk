import os, sys
import warnings
from IPython.core.display import HTML
from IPython.display import Image
from owslib.wms import WebMapService
from owslib.util import Authentication
from skimage import io
import requests
import authorisation_functions as auth

# turn off warnings (suppresses output from certification verification when verify=false)
warnings.simplefilter("ignore")


credentials = auth.import_credentials('credentials.json')
access_token = auth.generate_token(consumer_key=credentials['consumer_key'], consumer_secret=credentials['consumer_secret'])
print('Access token retrieved: ' + access_token)

service_url = 'https://view.eumetsat.int/geoserver/ows?'
wms = WebMapService(service_url, auth=Authentication(verify=False))
target_layer = 'msg_fes:ir108'#'msg_fes:rgb_natural'
print(HTML('<b>Layer title: </b>' + str(wms[target_layer].title)))
print(HTML('<b>CRS options: </b>' + str(wms[target_layer].crsOptions)))
print(HTML('<b>Bounding box: </b>' + str(wms[target_layer].boundingBox)))
print(HTML('<b>Layer abstract: </b>' + str(wms[target_layer].abstract)))
print(HTML('<b>Timestamp: </b>' + str(wms[target_layer].timepositions))) # by default WMS will return themost recent image


time_positions = wms[target_layer].timepositions
timestamp_html = '<b>Timestamp: </b>' + str(time_positions)

print(timestamp_html)

API_method = 'GetMap'

# check available format options
#for iter_format_option in wms.getOperationByName(API_method).formatOptions:
 #   print("Format option: ", iter_format_option)

# select format option
format_option = 'image/geotiff'

payload = {
    'layers' : [target_layer],
    'styles' : '',
    'format' : format_option,
    'crs'    : 'EPSG:4326',
    # 'bbox'   : (-77.7699966430664, -77.7699966430664, 77.7699966430664, 77.7699966430664),
   # 'bbox'   : (-45,35,45,62),
    'bbox'   : (-70,24,70,72),
    'size'   : (945,945),
    'time' : '2023-08-16T22:00:00.000Z/2023-08-16T22:00:00.000Z'
    #'size'   : (3840,2880)


    #'time' : '2020-06-18T14:00:00.000Z/2020-06-18T14:59:59.999Z'
}

wms = WebMapService(service_url, auth=Authentication(verify=False))
img = wms.getmap(**payload)
Image(img.read())
with open('../cut.tiff', 'wb') as f:
    f.write(img.read())

print('Bild wurde erfolgreich gespeichert.')
