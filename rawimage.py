from PIL import Image, ImageDraw
from time import clock
from os import path

class RawImage :

    def __init__(self, filename) :

        f, e = path.splitext(filename)
        desired = f + ".png"
        if filename != desired :
            try :
                print "Trying to convert file to PNG."
                Image.open(filename).save(desired)
            except IOError :
                print "Cannot convert file to PNG."
                return
        
        self.filename = desired

        self.im = Image.open(self.filename)
        self.format = self.im.format
        self.size = self.im.size

        print "\tReceiving raw data from image..." 
        self.raw_data = list(self.im.tobytes('raw'))
        self.bin_data = []
        self.msb_data = []

        dt = clock()
        
        print "\tProcessing raw data (this will take a minute)..."
        self.processRawData()    
        
        print "\tProcessing finished (%.2f seconds)." % (clock()-dt)

    def processRawData(self) :
        ''' Process the raw data by converting it to binary. '''
        inc = len(self.im.getbands())
        for i in range(0,len(self.raw_data),inc) :
            self.bin_data.append(self.hexToBinary( self.raw_data[i+x] for x in range(inc) ))
            self.msb_data.append(self.getMSB(self.bin_data[-1]))

    def hexToBinary(self, pix) :
        ''' Return the pixel in binary form (from hexidecimal). '''
        bina = []
        for i in pix :
            bina.append("%08d" % int(bin(ord(i))[2:]))
        return bina

    def binToDecimal(self, pix) :
        ''' Return the pixel in decimal form (from binary). '''
        deci = []
        for i in pix :
            deci.append(int(i,2))
        return deci

    def getLSB_xy(self, x, y) :
        ''' Return the least significant bits of the pixel at [x,y]. '''
        lsb = []
        for i in self.getPixel(x, y) :
            lsb.append(int(i[-1]))
        return lsb

    def getLSB_pix(self, pix) :
        ''' Return the least significant bits of the given pixel. ''' 
        lsb = []
        for i in pix :
            lsb.append(int(i[-1]))
        return lsb
    

    def getMSB(self, x, y) :
        ''' Return the most significant bits of the pixel. '''
        msb = []
        for i in self.getPixel(x, y) :
            msb.append(int(i[0]))
        return msb

    def getMSB(self, pix) :
        ''' Return the most significant bits of the given pixel. '''
        msb = []
        for i in pix :
            msb.append(int(i[0]))
        return msb

    def getPixel(self, x, y) :
        ''' Return the binary data of the pixel at [x,y]. '''
        return self.bin_data[y * self.size[0] + x]        

    def setPixel(self, x, y, fill) :
        ''' Set pixel at [x,y] to the colour of fill. '''
        self.raw_data[ y * self.size[0] + x ] = fill

    def calcNumCharacters(self) :
        ''' Returns the number of characters that can be stored in the image. '''
        return int(self.size[0] * self.size[1] * len(self.im.getbands()) / 8)

    def getBands(self) :
        ''' Return the number of bands in the image. '''
        return self.im.getbands()

    def saveImage(self, lsb) :
        ''' Save the changes made as a new image. '''
        self.new_im = self.im.copy()
        
        edit = ImageDraw.Draw(self.new_im)
        
        for row in range(len(lsb)) :
            for i in range(0,len(lsb[row]),len(self.getBands())) :
                newFill = []
                for j in range(len(self.getBands())) :
                    newFill.append(int(self.bin_data[row * self.size[0] + i/len(self.getBands())][j][:7] + str(lsb[row][i + j]),2))
                edit.point((int(i/len(self.getBands())),row),fill=tuple(newFill))
        del edit
        
        self.new_im.save(self.filename.split('.')[0] + "_encrypted.%s" % self.format.lower(), self.format)

        print "\tImage saved successfully as", self.filename.split('.')[0] + "_encrypted.%s" % self.format.lower()

            
            
        
