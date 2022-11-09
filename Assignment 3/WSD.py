import sys

while len(sys.argv) > 1:  # so long as arguments include files to open, assume only 1
    file = open(sys.argv[1])
    text = file.readlines()
    fold
