from YoukaiTools import AdvFunctions

#calculate different metrics about an image
def calculateAverageColor(image):
    div = image[0]*image[1]
    adder = [0]*image[2]
    for i in range(3, len(image)):
        for j in range(image[2]):
            adder[j] += image[i][j]
    for j in range(image[2]):
        adder[j] /= div
    return adder

def getColorAt(image, x, y):
    i = AdvFunctions.spatial.arrayIndex2To1(x, y, image[0], 3)
    return image[i]

