# Steganographic-Encryption-Program
A small program that can take text and store it securely inside of an image without changing the size of the file.
## Inspiration
I've been interested in cryptography for a while now, and at about this time last year I stumbled upon a Youtube video that explained what Steganography is and how it works. I immediately attempted to make my own form of a Steganography program, but it wasn't secure at all and was messily made. Now, I've spent a good amount of time building my own algorithm to encrypt a substantial amount of text within PNG images.
## What it does
Takes a text and image file input, and allows you to store the text within the image without altering the size of the image file, or changing the look of the picture (at least, that's what your eyes think). 
## How I built it
I used Python and a library named Pillow that allowed for easy interfacing image editing functions from the Pil library. 
## Challenges I ran into
Bug testing my algorithm was a huge pain, as you can only reasonably print pixel data to the screen when you're working with small images, and not big ones. 
Also, larger images (greater than 500x500) tend to take a long time to process. I'm still working on a way to optimize my algorithm so this doesn't happen.
## Accomplishments that I'm proud of
I'm proud of the fact that I was able to complete a project like this within the time frame of this hackathon. Usually I spend a lot of time staring at a wall trying to figure out the most efficient way to accomplish a goal, but I was able to speed up that process and managed to come out with a project to show my friends and family!
## What I learned
I learned that image editing is very difficult to do in a short amount of time, especially when you're working with a single pixel at once. I'm now interested in looking into algorithms to make this process faster.
## What's next for Steganographic Encryption Program
Optimization, and maybe scaling.
