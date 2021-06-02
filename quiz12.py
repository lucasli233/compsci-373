def createInitializedGreyscalePixelArray(image_width, image_height):
    return [[0]*image_width for _ in range(image_height)]


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    thresholded = createInitializedGreyscalePixelArray(
        image_width, image_height)
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


if __name__ == '__main__':
    image_width = 16
    image_height = 16
    pixel_array = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    (ccimg, ccsizes) = computeConnectedComponentLabeling(
        pixel_array, image_width, image_height)
    for i in range(len(ccimg)):
        print(ccimg[i])
    print(ccsizes)
