from eccodes import *
import sys
import traceback
import pandas as pd
import glob


#print(d.head())
#print(d.loc[d['Latitude']==52.464428])
#print(52.464428 in d.values)

INPUT = '/home/alex/Dokumente/BUFR/Neus'#sn.0010.bin''home/alex/'#
#VERBOSE = 1  # verbose error reporting
file_list = glob.glob(INPUT +'/*')#'bufr.out')#
d = pd.read_csv('../../documentation/StationSearchResults.csv')
print(file_list)
filterdlist =[]

def example(file):

    try:
        listofstations=[]

        # open bufr file
        f = open(file, 'rb')

        cnt = 0

        # loop for the messages in the file
        while 1:
            # get handle for message
            bufr = codes_bufr_new_from_file(f)
            if bufr is None:
                break

            print("message: %s" % cnt)

            # we need to instruct ecCodes to expand all the descriptors
            # i.e. unpack the data values
            codes_set(bufr, 'unpack', 1)
            #codes_set(bufr, 'skipExtraKeyAttributes', 1)

            #keyb = 'stationNumber'
            keyc= 'latitude'
            keyd= 'longitude'
            keye= 'pastWeather1'

            try:
                listofs=[round(codes_get(bufr, keyc),2),round(codes_get(bufr, keyd),2), codes_get(bufr,keye)] #,codes_get(bufr, keye)])
                if ((d['Latround'] == listofs[0]) & (d['Longround'] == listofs[1])).any() == True:
                    filterdlist.append([listofs])
                # delete handle

            except  ArrayTooSmallError as err:
                #print('Error with key="%s" : %s' % (keye, err.msg))
                pass
                #pass
                #print('Error with key="%s" : %s' % (keye, err.msg))
            except KeyValueNotFoundError:
                pass
            except SystemExit as er:
                #print('Error with key',  er.msg)
                pass
            cnt += 1
            codes_release(bufr)

    except SystemExit:
        pass
        # close the file
        f.close()





def main():
    for i in file_list:
        try:
            example(i)
        except SystemExit:
            break
    print("hier kommt der Filter", filterdlist)



if __name__ == "__main__":
    sys.exit(main())
