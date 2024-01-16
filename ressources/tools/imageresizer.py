from PIL import Image
import os
import argparse
from multiprocessing import Pool, cpu_count
import time
import glob
import numpy as np
def main(number):
    im = Image.open(files[number], mode='r')
    im1 = im.resize((resxa, resya), resample=Image.Resampling.LANCZOS)
    im1.save(outputpatha +"/"+ filenames[number], format='jpeg')
    im2 = im.resize((resxb, resyb), resample=Image.Resampling.LANCZOS)
    im2.save(outputpathb +"/"+ filenames[number], format='jpeg')
    #os.remove(levelname + filenames[number] + ".png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('outputpatha')
    parser.add_argument('outputpathb')
    parser.add_argument('inputpath')
    parser.add_argument('resxa')  # 350
    parser.add_argument('resya')  #
    parser.add_argument('resxb')
    parser.add_argument('resyb')
    args = parser.parse_args()  # gv[480#210    #480
    resxa= int(args.resxa)
    resxb = int(args.resxb)
    resya = int(args.resya)
    resyb = int(args.resyb)
    outputpatha = args.outputpatha
    outputpathb=args.outputpathb
    files= glob.glob(args.inputpath+"/*")
    filenames =[]
    for i in files:
        filenames.append(os.path.basename(i))
    number=np.arange(0,len(files))
    start_time = time.time()
    print(files)
    with Pool() as pool:
        pool.map(main, number)

    print("--- %s seconds ---" % (time.time() - start_time))