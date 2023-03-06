# Convert the BUFR message to JSON
from pybufrkit.renderer import FlatJsonRenderer
from pybufrkit.renderer import NestedJsonRenderer
from pybufrkit.decoder import Decoder
from pybufrkit.decoder import generate_bufr_message
from pybufrkit.encoder import Encoder
import pandas as pd
import json
import codecs
from tqdm import tqdm


encoder = Encoder()
decoder = Decoder()
#with open('/home/alex/Dokumente/BUFR/Neus/sn.0002.bin', 'rb') as ins:
 #      bufr_message = decoder.process(ins.read())
i=0
with open('/home/alex/Dokumente/BUFR/sn.0002.bin', 'rb') as ins:
    for bufr_message in tqdm(generate_bufr_message(decoder, ins.read())):
          # do something with the decoded message object
        json_data = NestedJsonRenderer().render(bufr_message)
        #print(json_data[0])
        if 307079 in ${%unexpanded_descriptors}: print(PBK_FILENAME)
        with open('jsons/'+str(i)+'.txt', 'w') as outs:
           outs.write(str(json_data))
        # Encode the JSON back to BUFR file
        i+=1


        #bufr_message_new = encoder.process(json_data)
        #with open('jsontest.bufr', 'wb') as outs:
         #   outs.write(bufr_message_new.serialized_bytes)

#d = pd.read_csv('../documentation/StationSearchResults.csv')

#filterdlist =[]
#f = codecs.open('/home/alex/y.json', 'r', encoding='utf-8')
#with codecs.open('/home/alex/y.json', 'r', encoding='utf-8',
 #                errors='ignore') as jsonfile:
#    data = json.load(jsonfile)