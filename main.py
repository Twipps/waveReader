# Using knowedge from my assembly class

# Reading the .WAV, mode rb is "read binary"
inputFile = open("C:\\Users\\jsuchovi\\Desktop\\Jump.wav", mode="rb")

# to traverse backwards for little endian
def LEByteRead(inData, position, stepsBack):
    returnArray = bytearray()
    for i in range(0, stepsBack):
        inData.seek(position)
        returnArray.extend(inData.read(1))
        position -= 1
    return returnArray

# the buffer index starts at zero
inputFileIdx = 0

# seek sets the input buffer pointer to only continue from that point.
chunkID = inputFile.read(4) # Big Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

chunkSize = LEByteRead(inputFile, inputFileIdx + 3, 4) # Little Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

format = inputFile.read(4) # Big Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx) 

subOneID = inputFile.read(4) # Big Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

subOneSize = LEByteRead(inputFile, inputFileIdx + 3, 4) # Little Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

audioFormat = LEByteRead(inputFile, inputFileIdx + 1, 2) # Little Endian, 1 = PCM, linear quantization
inputFileIdx += 2
inputFile.seek(inputFileIdx)

numberOfChannels = LEByteRead(inputFile, inputFileIdx + 1, 2) # Little Endian
inputFileIdx += 2
inputFile.seek(inputFileIdx)

sampleRate = LEByteRead(inputFile, inputFileIdx + 3, 4) # Little Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

byteRate = LEByteRead(inputFile, inputFileIdx + 3, 4) # Little Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

blockAlign = LEByteRead(inputFile, inputFileIdx + 1, 2)  # Little Endian
inputFileIdx += 2
inputFile.seek(inputFileIdx)

bitsPerSample = LEByteRead(inputFile, inputFileIdx + 1, 2) # Little Endian
inputFileIdx += 2
inputFile.seek(inputFileIdx)

subTwoID = inputFile.read(4) # Big Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

subTwoSize = LEByteRead(inputFile, inputFileIdx + 3, 4) # Little Endian
inputFileIdx += 4
inputFile.seek(inputFileIdx)

# converting the hex representation of binary into integers for readability
print("\n:: WAVE INPUT :: \n\nHeadID: " + str(chunkID) 
    + "\nHeadSize: " + str(int(chunkSize.hex(), 16))
    + "\nFormat: " + str(format)
    + "\n\nSubOneID: " + str(subOneID)
    + "\nSubOneSize: " + str(int(subOneSize.hex(), 16))
    + "\nAudioFormat: " + str(int(audioFormat.hex(), 16))
    + "\nNumberOfChannels: " + str(int(numberOfChannels.hex(), 16))
    + "\nSampleRate: " + str(int(sampleRate.hex(), 16))
    + "\nByteRate " + str(int(byteRate.hex(), 16))
    + "\nBlockAlign: " + str(int(blockAlign.hex(), 16))
    + "\nBitsPerSample: " + str(int(bitsPerSample.hex(), 16))
    + "\n\nSubTwoID: " + str(subTwoID)
    + "\nSubTwoSize: " + str(int(subTwoSize.hex(), 16)))

# 8 bit sound sampling, so every 8 bits is a sound sample.
# 16 bit signed sampling would require different jump distance.
inputFileIdx += int(subTwoSize.hex(), 16) - 1 # Subtracting one to line up for the loop
outString = ""

for i in range(0, int((int(subTwoSize.hex(), 16)))):
    soundData = LEByteRead(inputFile, inputFileIdx, 1) # one stepBack from the current position is 8 bytes

    inputFileIdx -= 1
    outString += str(soundData[0]) + " "

    if i % 4 == 0:
        outString += "\n"
    
print(outString)