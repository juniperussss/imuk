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
file_list = glob.glob(INPUT +'sn.0024.bin')
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

            #keyb = 'stationNumber'
            keyc= 'latitude'
            keyd= 'longitude'
            keye= 'pastWeather1'

            try:
                listofs=[round(codes_get(bufr, keyc),2),round(codes_get(bufr, keyd),2), codes_get(bufr,keye)] #,codes_get(bufr, keye)])
                if ((d['Latround'] == listofs[0]) & (d['Longround'] == listofs[1])).any() == True:
                    filterdlist.append([listofs])
                # delete handle
                codes_release(bufr)
            except CodesInternalError as err:

                pass
                #print('Error with key="%s" : %s' % (keye, err.msg))
            cnt += 1


        # close the file
        f.close()
        #print(listofstations)
        """"
        for j in range(len(listofstations)):
            if ((d['Latround'] == listofstations[j][0]) & (d['Longround'] == listofstations[j][1])).any() ==True:
                filterdlist.append([listofstations[j]])
        """
    print("hier kommt der Filter",filterdlist)


def main():
    try:
        example()
    except CodesInternalError as err:
        print(err)
        pass
        return 1


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
