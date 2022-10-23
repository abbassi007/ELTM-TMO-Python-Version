
from eltmtmo import eltm_tmo
from iohelper import ReadWriteFile
import numpy as np
from EadgeAwareFilter import filtring
import time

def main():
    
    start_time=time.time()
       
    readfile=ReadWriteFile("test//belgium.pfm")
    data,scale,width,height = readfile.readPFM()
    
    print('ELTM TMO!')
    print('Start converting HDR image to LDR image...')
    
    starttmo=eltm_tmo(data,scale,width,height)
    array=starttmo.tmo()
    ReadWriteFile.writePPM("test//test.ppm",width,height,np.int8(array))
    
    print('Converted to LDR image.')
    end_time=time.time()
    print('Execution time: {} seconds'.format(end_time-start_time))
    
if __name__=="__main__":
    main()