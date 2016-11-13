from rawimage import RawImage

class Decryption :

    def __init__(self, image) :
        self.image = image
        self.MAX_CHARACTERS = self.image.calcNumCharacters()
        self.NUM_BANDS = len(self.image.getBands())
        self.WIDTH = self.image.size[0]
        self.HEIGHT = self.image.size[1]
        self.END_SEQ = "11111111"

        self.lsb = []
        self.getLSB()

    def decryptMessage(self) :
        ''' Handle decrypting a message from an image. Return True if successful, False otherwise. '''

        print "\tDecrypting image..."

        shortSide = min(self.HEIGHT,self.WIDTH*self.NUM_BANDS)
        for i in range(int(shortSide/2)-1,-1,-1) :
            '''
            if self.lsb[i][i] == 1 :
                #print "Shifting UP at [%d]" % (i)
                self.verticalShift(self.WIDTH*self.NUM_BANDS, self.HEIGHT, i+1, -1)
            else :
                #print "Shifting LEFT at [%d]" % (i)
                self.horizontalShift(self.WIDTH*self.NUM_BANDS, self.HEIGHT, i+1, -1)
            '''
            if self.lsb[i][i] == 1 :
                #print "Rotating CCW at [%d]" % (i)
                self.rotateCCW(self.WIDTH*self.NUM_BANDS, self.HEIGHT,i+1)
            else :
                #print "Rotating CW at [%d]" % (i)
                self.rotateCW(self.WIDTH*self.NUM_BANDS, self.HEIGHT,i+1)
                
        #self.rotateCCW(self.WIDTH*self.NUM_BANDS,self.HEIGHT, 0)
        #self.verticalShift(self.WIDTH*self.NUM_BANDS,self.HEIGHT,0,-1)

        binaMess = ""
        for i in range(len(self.lsb) * len(self.lsb[0])) :
                binaMess += str(self.lsb[int(i/len(self.lsb[0]))][i % len(self.lsb[0])])
                if binaMess[-8:] == self.END_SEQ and len(binaMess[:-8])%8==0 :
                    binaMess = binaMess[:-8]
                    break
                

        binaMess = self.xor([binaMess] + self.getMSB(len(binaMess)))
        
        binaMess = (8*(len(binaMess)%8!=0) - (len(binaMess)%8)) * "0" + binaMess
        
        mess = ""
        for i in range(0,len(binaMess), 8) :
            mess += chr(int(binaMess[i:i+8],2))
        return mess

        
        
                 
    def xor(self, binaList) :
        ''' Return the XOR of the binary strings given. '''
        bina = bin(int(binaList[0],2))[2:]
        for i in range(1,len(binaList)) :
            bina = bin(int(bina,2) ^ int(binaList[i],2))[2:]
        return bina

    def getMSB(self, n) :
        ''' Get the first n MSB for each band in the image. '''
        msb = [""]*self.NUM_BANDS
        for i in range(n) :
            for j in range(self.NUM_BANDS) :
                msb[j] += str(self.image.msb_data[i%(n/self.NUM_BANDS)][j])
        return msb 

    def getLSB(self) :
        ''' Get the LSB to process. '''
        for y in range(self.HEIGHT) :
            row = []
            for x in range(self.WIDTH) :
                for i in self.image.getLSB_xy(x,y) :
                    row.append(i)
            self.lsb.append(row)

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


        
