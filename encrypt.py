from random import getrandbits
from rawimage import RawImage
from time import clock

class Encryption :

    def __init__(self, image) :
        self.image = image
        self.MAX_CHARACTERS = self.image.calcNumCharacters()
        self.NUM_BANDS = len(self.image.getBands())
        self.WIDTH = self.image.size[0]
        self.HEIGHT = self.image.size[1]
        self.END_SEQ = "11111111"

        self.lsb = []


    def encryptMessage(self, mess) :
        ''' Handle encrypting a message within the image. Return True is success, False otherwise.'''

        print "\tChecking message validity."
        binaMess = self.messageToBinary(mess)

        if binaMess is None : return False

        print "\tMessage is valid. Encrypting into image."
        
        self.createLSB(binaMess)

        #self.verticalShift(self.WIDTH*self.NUM_BANDS,self.HEIGHT, 0, 1)
        #self.rotateCW(self.WIDTH*self.NUM_BANDS,self.HEIGHT, 0)

        dt = clock()

        shortSide = min(self.HEIGHT, self.WIDTH*self.NUM_BANDS)
        for i in range(int(shortSide/2)) :
            
            if self.lsb[i][i] == 1 :
                #print "Rotating CW at [%d]" % (i)
                self.rotateCW(self.WIDTH*self.NUM_BANDS, self.HEIGHT, i+1)
            else :
                #print "Rotating CCW at [%d]" % (i)
                self.rotateCCW(self.WIDTH*self.NUM_BANDS, self.HEIGHT, i+1)
            '''
            if i % 5 == 0 : print clock()-dt
            if self.lsb[i][i] == 1 :
                #print "Shifting DOWN at [%d]" % (i)
                self.verticalShift(self.WIDTH*self.NUM_BANDS, self.HEIGHT, i+1, 1)
            else :
                #print "Shifting RIGHT at [%d]" % (i)
                self.horizontalShift(self.WIDTH*self.NUM_BANDS, self.HEIGHT, i+1, 1)
            '''
        print "\tMessage is encrypted in image. Saving image."

        self.image.saveImage(self.lsb)

        return True
        
    def createLSB(self, mess) :
        ''' Create a custom random LSB as noise following the given binary message. '''
        ind = 0
        for i in range(self.HEIGHT) :
            row = []
            for j in range(self.WIDTH) :
                for k in range(self.NUM_BANDS) :
                    if ind < len(mess) :
                        row.append(int(mess[ind]))
                        ind+=1
                    else :
                        row.append(int(getrandbits(1)))
            self.lsb.append(row)

    def messageToBinary(self, mess) :
        ''' Convert a message string into binary. '''
        length = (len(mess)*8 + len(self.END_SEQ))/8
        if length >= self.MAX_CHARACTERS :
            print "\nERROR: message too long to encrypt in image.\n"
            return None
        bina = ""
        for letter in mess :
            bina += "%08d" % int(bin(ord(letter))[2:])

        return self.xor([bina] + self.getMSB(len(bina))) + self.END_SEQ

    def xor(self, binaList) :
        ''' Return the XOR of the binary strings given. '''
        bina = bin(int(binaList[0],2))[2:]
        for i in range(1,len(binaList)) :
            bina = bin(int(bina,2) ^ int(binaList[i],2))[2:]
        return (8*(len(bina)%8!=0) - (len(bina)%8)) * "0" + bina

    def getMSB(self, n) :
        ''' Get the first n MSB for each band in the image. '''
        msb = [""]*self.NUM_BANDS
        
        for i in range(n) :
            for j in range(self.NUM_BANDS) :
                msb[j] += str(self.image.msb_data[i%(n/self.NUM_BANDS)][j])
        return msb
                
    def rotateCCW(self, w, h, off) :
        ''' Rotate a ring of LSB 90 degrees counter-clockwise. '''
        for i in range(0 + off, w-1 - off) :
            self.swap([0 + off,i],[0 + off,i+1])

        for i in range(0 + off, h-1 - off) :
            self.swap([i,w-1 - off],[i+1,w-1 - off])

        for i in range(w-1 - off, 0 + off, -1) :
            self.swap([h-1 - off,i],[h-1 - off,i-1])

        for i in range(h-1 - off, 1 + off, -1) :
            self.swap([i,0 + off],[i-1,0 + off])

    def rotateCW(self, w, h, off) :
        ''' Rotate a ring of LSB 90 degrees clockwise. '''
        for i in range(1 + off,h-1 - off) :
            self.swap([i,0 + off],[i+1,0 + off])

        for i in range(0 + off,w-1 - off) :
            self.swap([h-1 - off,i],[h-1 - off,i+1])

        for i in range(h-1 - off,0 + off, -1) :
            self.swap([i,w-1 - off],[i-1,w-1 - off])
            
        for i in range(w-1 - off,0 + off, -1) :
            self.swap([0 + off,i],[0 + off,i-1])

    def horizontalShift(self, w, h, off, di) :
        ''' Shift the items in every other row one spot in the given direction. '''
        for hor in range(h) :
            if (hor+off) % 2 == 0 :
                if di == 1 :
                    temp = self.lsb[hor][-1]
                    for item in range(w-1,0,-1) :
                        self.lsb[hor][item] = self.lsb[hor][item-1]
                    self.lsb[hor][0] = temp
                elif di == -1 :
                    temp = self.lsb[hor][0]
                    for item in range(1,w) :
                        self.lsb[hor][item-1] = self.lsb[hor][item]
                    self.lsb[hor][-1] = temp
            
            
    def verticalShift(self, w, h, off, di) :
        ''' Shift the items in every other column one spot in the given direction. '''
        for col in range(w) :
            if (col+off) % 2 == 0 :
                if di == 1 :
                    temp = self.lsb[-1][col]
                    for item in range(h-1,0,-1) :
                        self.lsb[item][col] = self.lsb[item-1][col]
                    self.lsb[0][col] = temp
            
                elif di == -1 :
                    temp = self.lsb[0][col]
                    for item in range(1,h) :
                        self.lsb[item-1][col] = self.lsb[item][col]
                    self.lsb[-1][col] = temp
            
            
    def swap(self, p1, p2) :
        ''' Swap the LSB of the two points given. '''
        temp = self.lsb[p1[0]][p1[1]]
        self.lsb[p1[0]][p1[1]] = self.lsb[p2[0]][p2[1]]
        self.lsb[p2[0]][p2[1]] = temp

