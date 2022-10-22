import numpy as np


class ReadWriteFile:
    
    """In this ReadWritelFile class we have two methods:
    1:  First method is for the reading of high dynamic range(HDR) 
        pfm file which is 32 bit image.
    2:  Second method is for the writing of low dynamic range(LDR) 
        ppm file which is 8 bit image.
    """
    
    def __init__(self, filename):
        self.filename=filename
        
    def readPFM(self):
        with open(self.filename, "rb") as file:

            color = width = height = scale = endian = None
            
            header = file.readline().rstrip().decode('latin-1')
            
            if header == 'PF':
                color = True
            elif header == 'Pf':
                color = False
            else:
                raise Exception('Not a PFM file.')

            width = int(file.readline().rstrip())
            height = int(file.readline().rstrip())
            
            
            scale = float(file.readline().rstrip())
            
            if scale < 0:  # little-endian
                endian = '<'
                scale = -scale
            else:
                endian = '>'  # big-endian

            data = np.fromfile(file, endian + 'f')
            shape = (height, width, 3) if color else (height, width)
            data = data.reshape(shape)
            #data = np.flipud(data)*scale
        return data, scale, width,height
    
    def writePPM(filename, width, height,data):
        with open(filename,"wb") as file:
            ppm_header = f'P6\n{width} {height}\n255\n'
            file.write(bytearray(ppm_header,'ascii'))
            file.write(data)
        file.close()
