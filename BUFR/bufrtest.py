from eccodes import *
import sys
import traceback
import pandas as pd
import glob


#print(d.head())
#print(d.loc[d['Latitude']==52.464428])
#print(52.464428 in d.values)

INPUT = '/home/alex/Dokumente/BUFR/'#sn.0010.bin'
#VERBOSE = 1  # verbose error reporting
file_list = glob.glob(INPUT +'sn.0000.bin')
d = pd.read_csv('../documentation/StationSearchResults.csv')
print(file_list)
filterdlist =[]

def example():
    for i in file_list:
        listofstations=[]

        # open bufr file
        f = open(i, 'rb')

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

            # ---------------------------------------------
            # get values for keys holding a single value
            # ---------------------------------------------
            # Native type integer

            #key = 'blockNumber'
            """
            try:
                print('  %s: %s' % (key, codes_get(bufr, key)))
            except CodesInternalError as err:
                print('Error with key="%s" : %s' % (key, err.msg))


            # Native type integer
            key = 'stationOrSitename'
            try:
                print('  %s: %s' % (key, codes_get(bufr, key)))
            except CodesInternalError as err:
                print('Error with key="%s" : %s' % (key, err.msg))

            """
            # Native type float
            #keyb = 'stationNumber'
            keyc= 'latitude'
            keyd= 'longitude'
            keye= 'pastWeather1'

            """
            try:
                print('  %s: %s' % (keyb, codes_get(bufr, keyb)))
            except CodesInternalError as err:
                print('Error with key="%s" : %s' % (keyb, err.msg))
            """
            try:
                listofstations.append([codes_get(bufr, keyc),codes_get(bufr, keyd)]) #,codes_get(bufr, keye)])
            except CodesInternalError as err:
                pass
                #print('Error with key="%s" : %s' % (keye, err.msg))
            """
            # Native type string
            key = 'stationOrSitename'
            try:
                print('  %s: %s' % (key, codes_get(bufr, key)))
            except CodesInternalError as err:
                print('Error with key="%s" : %s' % (key, err.msg))
            #----------------------------
            # get values for an array
            # --------------------------------
            # Native type integer

            key = 'bufrdcExpandedDescriptors'

            # get size
            num = codes_get_size(bufr, key)
            print('  size of %s is: %s' % (key, num))

            # get values
            values = codes_get_array(bufr, key)
            for i in range(len(values)):
                print("   %d %06d" % (i + 1, values[i]))

            # Native type float
            key = 'numericValues'

            # get size
            num = codes_get_size(bufr, key)
            print('  size of %s is: %s' % (key, num))

            # get values
            values = codes_get_array(bufr, key)
            for i in range(len(values)):
                print("   %d %.10e" % (i + 1, values[i]))

            """
            # ----
            cnt += 1

            # delete handle
            codes_release(bufr)

        # close the file
        f.close()

        #print(listofstations)
        for j in range(len(listofstations)):
            if (listofstations[j][0] in d.Latitude.values) ==True and (listofstations[j][1] in d.Latitude.values):
                filterdlist.append([listofstations[j]])



def main():
    try:
        example()
    except CodesInternalError as err:
        pass
        return 1

    print(filterdlist)
    """
    try:
        example()
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')

        return 1
        """


if __name__ == "__main__":
    sys.exit(main())
