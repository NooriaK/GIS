inputFC = r"C:\Users\Noori\Downloads\PythEveryone\HandleErrors\SanDiego.gdb\SD_Stream"
outputFC = "StreamBuffers_A"
bufferField = "BufferDistance"
bufferUnit = "Feet"
dissolveType = "ALL"

samplesA = [95, 99, 105, 106, 110]
samplesB = [451, 485, 502, 520, 535]
samplesC = [910, 945, 996, 1055, 1120]

import statistics


sampleMeans = [samplesA, samplesB, samplesC]
buffDists = []
for values in sampleMeans:
    print(str(values) + " is processing")
    meanValue = statistics.mean(values)
    buffDists.append(meanValue)
print(buffDists)

#Use the Multiple Ring Buffer geoprocessing tool

import arcpy

arcpy.analysis.MultipleRingBuffer(inputFC, outputFC, buffDists, bufferUnit, bufferField, dissolveType)




