from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

import imageIO.png


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage
    
# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)

    for i in range(0, image_height):
        for j in range(0, image_width):
            greyscale_pixel_array[i][j] = round(0.299*pixel_array_r[i][j] + 0.587*pixel_array_g[i][j] + 0.114*pixel_array_b[i][j])

    return greyscale_pixel_array

def computeMinAndMaxValues(pixel_array, image_width, image_height):
    f_low = 999999
    f_high = 0
    for i in range(0, image_height):
        for j in range(0, image_width):
            if pixel_array[i][j] < f_low:
                f_low = pixel_array[i][j]
            if pixel_array[i][j] > f_high:
                f_high = pixel_array[i][j]
    return (f_low, f_high)

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    (f_low, f_high) = computeMinAndMaxValues(pixel_array, image_width, image_height)
    g_min = 0
    g_max = 255
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(0, image_height):
        for j in range(0, image_width):
            if f_high - f_low == 0:
                greyscale_pixel_array[i][j] = 0
            else:
                s_out = (pixel_array[i][j] - f_low)*((g_max - g_min)/(f_high - f_low)) + g_min
            if s_out < g_min:
                greyscale_pixel_array[i][j] = round(g_min)
            if g_min <= s_out and s_out <= g_max:
                greyscale_pixel_array[i][j] = round(s_out)
            if s_out > g_max:
                greyscale_pixel_array[i][j] = round(g_max)

    return greyscale_pixel_array

def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    horizontal_edges = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(0, image_height):
        for j in range(0, image_width):
            if i == 0 or j == 0 or i == image_height-1 or j == image_width-1:
                horizontal_edges[i][j] = 0.0
            else:
                horizontal_edges[i][j] = abs((1/8)*(-pixel_array[i-1][j-1] - 2*pixel_array[i][j-1] - pixel_array[i+1][j-1] + pixel_array[i-1][j+1] + 2*pixel_array[i][j+1] + pixel_array[i+1][j+1]))
    return horizontal_edges

def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    vertical_edges = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(0, image_height):
        for j in range(0, image_width):
            if i == 0 or j == 0 or i == image_height-1 or j == image_width-1:
                vertical_edges[i][j] = 0.0
            else:
                vertical_edges[i][j] = abs((1/8)*(pixel_array[i-1][j-1] + 2*pixel_array[i-1][j] + pixel_array[i-1][j+1] - pixel_array[i+1][j-1] - 2*pixel_array[i+1][j] - pixel_array[i+1][j+1]))
    return vertical_edges

def computeMagnitude(vertical, horizontal, image_width, image_height):
    magnitude = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(0, image_height):
        for j in range(0, image_width):
            magnitude[i][j] = vertical[i][j] + horizontal[i][j]
    
    return magnitude

def computeBoxAveraging3x3(pixel_array, image_width, image_height):
    box_average = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(0, image_height):
        for j in range(0, image_width):
            if i == 0 or j == 0 or i == image_height-1 or j == image_width-1:
                box_average[i][j] = 0
            else:
                box_average[i][j] = abs(1/9*(pixel_array[i-1][j-1] + pixel_array[i-1][j] + pixel_array[i-1][j+1] + pixel_array[i][j-1] + pixel_array[i][j] + pixel_array[i][j+1] + pixel_array[i+1][j-1] + pixel_array[i+1][j] + pixel_array[i+1][j+1]))
    return box_average

def computeGaussianAveraging3x3RepeatBorder(pixel_array, image_width, image_height):
    gaussian_average = createInitializedGreyscalePixelArray(image_width, image_height)

    padded_pixel_array = createInitializedGreyscalePixelArray(image_width+2, image_height+2)

    for i in range(0, image_height):
        for j in range(0, image_width):
            padded_pixel_array[i+1][j+1] = pixel_array[i][j]
        
    for i in range(0, image_height+2):
        for j in range(0, image_width+2):
            if i==1 and j == 1:
                padded_pixel_array[i-1][j-1] = padded_pixel_array[i][j]
            if i == 1:
                padded_pixel_array[i-1][j] = padded_pixel_array[i][j]
            if i == image_height+2-1-1:
                padded_pixel_array[i+1][j] = padded_pixel_array[i][j]
            if j == 1:
                padded_pixel_array[i][j-1] = padded_pixel_array[i][j]
            if j == image_width+2-1-1:
                padded_pixel_array[i][j+1] = padded_pixel_array[i][j]

    for i in range(0, image_height):
        for j in range(0, image_width):
            gaussian_average[i][j] = (padded_pixel_array[i+1-1][j+1-1] + 2*padded_pixel_array[i+1-1][j+1] + padded_pixel_array[i+1-1][j+1+1] + 2*padded_pixel_array[i+1][j+1-1] + 4*padded_pixel_array[i+1][j+1] + 2*padded_pixel_array[i+1][j+1+1] + padded_pixel_array[i+1+1][j+1-1] + 2*padded_pixel_array[i+1+1][j+1] + padded_pixel_array[i+1+1][j+1+1]) / 16

    return gaussian_average

def computeThreshold(pixel_array, threshold_value, image_width, image_height):

    thresholded = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(0, image_height):
        for j in range(0, image_width):
            if pixel_array[i][j] < threshold_value:
                thresholded[i][j] = 0
            else:
                thresholded[i][j] = 255
    
    return thresholded

def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    eroded = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(1, image_height-1):
        for j in range(1, image_width-1):
            temp = (pixel_array[i-1][j-1] * pixel_array[i-1][j] * pixel_array[i-1][j+1] *
                    pixel_array[i][j-1] * pixel_array[i][j] * pixel_array[i][j+1] *
                    pixel_array[i+1][j-1] * pixel_array[i+1][j] * pixel_array[i+1][j+1])

            if temp != 0:
                eroded[i][j] = 1
            else:
                eroded[i][j] = 0

    return eroded

def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):

    padded = createInitializedGreyscalePixelArray(
        image_width+2, image_height+2)

    for i in range(0, image_height):
        for j in range(0, image_width):
            padded[i+1][j+1] = pixel_array[i][j]

    dilated = createInitializedGreyscalePixelArray(image_width, image_height)

    for i in range(0, image_height):
        for j in range(0, image_width):
            temp = (padded[i+1-1][j+1-1] + padded[i+1-1][j+1] + padded[i+1-1][j+1+1] +
                    padded[i+1][j+1-1] + padded[i+1][j+1] + padded[i+1][j+1+1] +
                    padded[i+1+1][j+1-1] + padded[i+1+1][j+1] + padded[i+1+1][j+1+1])

            if temp != 0:
                dilated[i][j] = 1
            else:
                dilated[i][j] = 0

    return dilated

def computeConnectedComponentLabeling(pixel_array, image_width, image_height):

    ccimg = createInitializedGreyscalePixelArray(image_width, image_height)
    visited = createInitializedGreyscalePixelArray(image_width, image_height)
    label = 1
    ccsizes = {}

    for i in range(0, image_height):
        for j in range(0, image_width):

            if pixel_array[i][j] != 0 and visited[i][j] == 0:
                count = 0
                queue = Queue()
                queue.enqueue((i, j))

                while queue.isEmpty() == False:
                    (x, y) = queue.dequeue()
                    ccimg[x][y] = label
                    visited[x][y] = 1
                    count += 1

                    if x-1 >= 0 and pixel_array[x-1][y] != 0 and visited[x-1][y] == 0:
                        queue.enqueue((x-1, y))
                        visited[x-1][y] = 1
                    if x + 1 < image_height and pixel_array[x+1][y] != 0 and visited[x+1][y] == 0:
                        queue.enqueue((x+1, y))
                        visited[x+1][y] = 1
                    if y >= 0 and pixel_array[x][y-1] != 0 and visited[x][y-1] == 0:
                        queue.enqueue((x, y-1))
                        visited[x][y-1] = 1
                    if y+1 < image_width and pixel_array[x][y+1] != 0 and visited[x][y+1] == 0:
                        queue.enqueue((x, y+1))
                        visited[x][y+1] = 1

                ccsizes[label] = count
                label += 1

    return ccimg, ccsizes

def computeEdges(pixel_array, ccsizes, image_width, image_height):
    largestComponent = createInitializedGreyscalePixelArray(image_width, image_height)
    largestComponent_size = 0
    largestComponent_lable = 0
    for lable in ccsizes.keys():
        if ccsizes[lable] > largestComponent_size:
            largestComponent_size = ccsizes[lable]
            largestComponent_lable = lable

    minh = image_height
    maxh = 0
    minw = image_width
    maxw = 0
    
    for i in range(0, image_height):
        for j in range(0, image_width):
            if pixel_array[i][j] == largestComponent_lable:
                largestComponent[i][j] = 255
                if i < minh:
                    minh = i
                if i > maxh:
                    maxh = i
                if j < minw:
                    minw = j
                if j > maxw:
                    maxw = j

            else:
                largestComponent[i][j] = 0
            
    return(largestComponent, minw, maxw, minh, maxh)

def computeEdgePointsForRotated(largestComponent, minw, maxw, minh, maxh, image_width, image_height): 
    pointA, pointB, pointC, pointD = 0, 0, 0, 0
    for i in range(0, image_height):
        for j in range(0, image_width):
            if largestComponent[i][j] == 255:
                if j == minw:
                    pointA = (j, i)
                if i == minh:
                    pointB = (j, i)
                if j == maxw:
                    pointC = (j, i)
                if i == maxh:
                    pointD = (j, i)
    
    return (pointA, pointB, pointC, pointD)


def main():
    poster1small = "./images/covid19QRCode/poster1small.png"
    bch = "./images/covid19QRCode/challenging/bch.png"
    bloomfield = "./images/covid19QRCode/challenging/bloomfield.png"
    connecticut = "./images/covid19QRCode/challenging/connecticut.png"
    playground = "./images/covid19QRCode/challenging/playground.png"
    poster1smallrotated = "./images/covid19QRCode/challenging/poster1smallrotated.png"
    shanghai = "./images/covid19QRCode/challenging/shanghai.png"
    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(poster1small)

    # step 1
    greyscale = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    scaled = scaleTo0And255AndQuantize(greyscale, image_width, image_height)
    
    # step 2
    abs_horizontal_edges = computeHorizontalEdgesSobelAbsolute(scaled, image_width, image_height)
    
    # step 3
    abs_vertical_edges = computeVerticalEdgesSobelAbsolute(scaled, image_width, image_height)
    
    # step 4
    magnitude = computeMagnitude(abs_vertical_edges, abs_horizontal_edges, image_width, image_height)

    # step 5

    smoothed = magnitude
    for _ in range(1):
        smoothed = computeBoxAveraging3x3(smoothed, image_width, image_height)
        smoothed = scaleTo0And255AndQuantize(smoothed, image_width, image_height)
    
    # step 6

    threshold = computeThreshold(smoothed, 90, image_width, image_height)

    # step 7
    dilated = computeDilation8Nbh3x3FlatSE(threshold, image_width, image_height)
    eroded = computeErosion8Nbh3x3FlatSE(dilated, image_width, image_height)

    # step 8
    (ccimg, ccsizes) = computeConnectedComponentLabeling(eroded, image_width, image_height)

    # step 9
    (largestComponent, minw, maxw, minh, maxh) = computeEdges(ccimg, ccsizes, image_width, image_height)

    (pointA, pointB, pointC, pointD) = computeEdgePointsForRotated(largestComponent, minw, maxw, minh, maxh, image_width, image_height)

    origionalRGB = prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height)

    # pyplot.imshow(onlyQR, cmap="gray")
    pyplot.imshow(origionalRGB)

    # get access to the current pyplot figure
    axes = pyplot.gca()

    # print out only the QR code
    # axes.set_xlim((minw,maxw))
    # axes.set_ylim((minh,maxh))

    rect = Rectangle( (minw, minh), maxw - minw, maxh - minh, linewidth=3, edgecolor='g', facecolor='none')
    axes.add_patch(rect)

    # polygon = Polygon((pointA, pointB, pointC, pointD), linewidth=3, edgecolor='red', facecolor='none')
    # axes.add_patch(polygon)

    # plot the current figure
    pyplot.show()



if __name__ == "__main__":
    main()