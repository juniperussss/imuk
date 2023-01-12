from pybufrkit.decoder import Decoder
import json
decoder = Decoder()
with open("sn.0001.bin", 'rb') as ins:
    bufr_message = decoder.process(ins.read())

# Convert the BUFR message to JSON
from pybufrkit.renderer import FlatJsonRenderer
json_data = FlatJsonRenderer().render(bufr_message)

with open("sn.0001.bin", 'rb') as ins:
    bufr_message = decoder.process(ins.read())
print(json_data[1])