





def createInitializedGreyscalePixelArray(image_width, image_height):
  return [[0]*image_width for _ in range(image_height)]

def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
  horizontal_edges = createInitializedGreyscalePixelArray(image_width, image_height)
  for i in range(0, image_height):
    for j in range(0, image_width):
      if i == 0 or j == 0 or i == image_height-1 or j == image_width-1:
        horizontal_edges[i][j] = 0
      else:
        horizontal_edges[i][j] = abs(1/8*(-pixel_array[i-1][j-1] - 2*pixel_array[i][j-1] - pixel_array[i+1][j-1] + pixel_array[i-1][j+1] + 2*pixel_array[i][j+1] + pixel_array[i+1][j+1]))
  return horizontal_edges

def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
  vertical_edges = createInitializedGreyscalePixelArray(image_width, image_height)
  for i in range(0, image_height):
    for j in range(0, image_width):
      if i == 0 or j == 0 or i == image_height-1 or j == image_width-1:
        vertical_edges[i][j] = 0
      else:
        vertical_edges[i][j] = abs(1/8*(pixel_array[i-1][j-1] + 2*pixel_array[i-1][j] + pixel_array[i-1][j+1] - pixel_array[i+1][j-1] - 2*pixel_array[i+1][j] - pixel_array[i+1][j+1]))
  return vertical_edges

def computeBoxAveraging3x3(pixel_array, image_width, image_height):
  box_average = createInitializedGreyscalePixelArray(image_width, image_height)
  for i in range(0, image_height):
    for j in range(0, image_width):
      if i == 0 or j == 0 or i == image_height-1 or j == image_width-1:
        box_average[i][j] = 0
      else:
        box_average[i][j] = abs(1/9*(pixel_array[i-1][j-1] + pixel_array[i-1][j] + pixel_array[i-1][j+1] + pixel_array[i][j-1] + pixel_array[i][j] + pixel_array[i][j+1] + pixel_array[i+1][j-1] + pixel_array[i+1][j] + pixel_array[i+1][j+1]))
  return box_average

def computeMedian5x3ZeroPadding(pixel_array, image_width, image_height):
  box_median = createInitializedGreyscalePixelArray(image_width, image_height)

  padded_pixel_array = createInitializedGreyscalePixelArray(image_width+4, image_height+2)
  for i in range(0, image_height):
    for j in range(0, image_width):
      padded_pixel_array[i+1][j+2] = pixel_array[i][j]

  for i in range(0, image_height):
    for j in range(0, image_width):
      boxlist = sorted([padded_pixel_array[i+1-1][j+2-2], padded_pixel_array[i+1-1][j+2-1], padded_pixel_array[i+1-1][j+2], padded_pixel_array[i+1-1][j+2+1], padded_pixel_array[i+1-1][j+2+2],
      padded_pixel_array[i+1][j+2-2], padded_pixel_array[i+1][j+2-1], padded_pixel_array[i+1][j+2], padded_pixel_array[i+1][j+2+1], padded_pixel_array[i+1][j+2+2],
      padded_pixel_array[i+1+1][j+2-2], padded_pixel_array[i+1+1][j+2-1], padded_pixel_array[i+1+1][j+2], padded_pixel_array[i+1+1][j+2+1], padded_pixel_array[i+1+1][j+2+2]])
      box_median[i][j] = boxlist[7]

  return box_median

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

if __name__ == '__main__':
  image_width = 6
  image_height = 5
  pixel_array = [ [6, 3, 2, 6, 4, 7], 
                  [5, 3, 2, 7, 0, 6], 
                  [6, 2, 7, 7, 1, 7], 
                  [7, 6, 6, 2, 7, 3], 
                  [2, 2, 2, 5, 1, 2] ]
  print(computeGaussianAveraging3x3RepeatBorder(pixel_array, image_width, image_height))