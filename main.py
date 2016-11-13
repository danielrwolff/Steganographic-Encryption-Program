from encrypt import Encryption
from decrypt import Decryption
from rawimage import RawImage
import os

def loadImage(filename) :
    if os.path.isfile(filename) :
        print "\tOpening", filename
        images.append([RawImage(filename),filename])
    else :
        print "\tImage not found!"

print "====================================================="
print "| Welcome to the Steganographic Encryption Program! |"
print "====================================================="
print ""
print "> Type 'help' to get a list of commands."
print "> Type 'quit' to exit the program at any time."
print ">"

doQuit = False
images = []

while not doQuit :
    switch = raw_input("> ").split()

    if switch[0] == 'quit' : doQuit = True
    elif switch[0] == 'help' :
        print "\t'quit' -> Type to exit program."
        print "\t'load' [FILENAME] -> Type to load an image."
        print "\t'list' -> List the loaded image names."
        print "\t'encrypt' [FILENAME] -> Type to encrypt text within an image of FILENAME."
        print "\t'decrypt' [FILENAME] -> Type to decrypt text from an image of FILENAME."
        
    elif switch[0] == 'load' :
        loadImage(switch[1])
    elif switch[0] == 'list' :
        for i in images: print "\t",i[1]
    elif switch[0] == 'encrypt' :
        isLoaded = False
        for i in images :
            if switch[1] == i[1] :
                isLoaded = True
                print '\t' + i[1] + " found!"
                Encryption(i[0]).encryptMessage(
                    raw_input("\tEnter the message to encrypt in the image: ")
                    )
                print ""
                loadImage(os.path.splitext(switch[1])[0] + "_encrypted" + os.path.splitext(switch[1])[1])
        if not isLoaded : print "\tImage not loaded!"
    elif switch[0] == 'decrypt' :
        isLoaded = False
        for i in images :
            if switch[1] == i[1] :
                isLoaded = True
                print '\t' + i[1] + " found!"
                print Decryption(i[0]).decryptMessage()
                print ""
        if not isLoaded : print "\tImage not loaded!"
        
            
print "> Thanks for using the Steganographic Encryption Program!"
