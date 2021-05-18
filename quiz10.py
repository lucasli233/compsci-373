# Q1

def computeHistogram(pixel_array, image_width, image_height, nr_bins):
  res = []
  for x in range(0, nr_bins):
    intensity = 0.0
    for i in range(0, image_height):
      for j in range(0, image_width):
        if pixel_array[i][j] == x:
          intensity += 1.0
    res.append(intensity)
  return res

# Q2

def computeCumulativeHistogram(pixel_array, image_width, image_height, nr_bins):
  res = []
  intensity = 0.0
  for x in range(0, nr_bins):
    for i in range(0, image_height):
      for j in range(0, image_width):
        if pixel_array[i][j] == x:
          intensity += 1.0
    res.append(intensity)
  return res

# Q3

def createInitializedGreyscalePixelArray(image_width, image_height):
  return [[None]*image_width for _ in range(image_height)]

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
  greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
  # STUDENT CODE HERE
  for i in range(0, image_height):
    for j in range(0, image_width):
      greyscale_pixel_array[i][j] = round(0.299*pixel_array_r[i][j] + 0.587*pixel_array_g[i][j] + 0.114*pixel_array_b[i][j])

  return greyscale_pixel_array

# Q4

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

if __name__ == '__main__':
  # Q1
  # image_width = 6
  # image_height = 5
  # pixel_array = [ [3, 7, 2, 3, 2, 3], 
  #                 [0, 4, 6, 1, 4, 4], 
  #                 [3, 1, 2, 5, 2, 2], 
  #                 [1, 6, 3, 1, 5, 2], 
  #                 [4, 4, 6, 5, 0, 0] ]
  # nr_bins = 8
  # histogram = computeHistogram(pixel_array, image_width, image_height, nr_bins)
  # print(histogram)

  # Q2
  # image_width = 6
  # image_height = 5
  # pixel_array = [ [3, 7, 2, 3, 2, 3], 
  #                 [0, 4, 6, 1, 4, 4], 
  #                 [3, 1, 2, 5, 2, 2], 
  #                 [1, 6, 3, 1, 5, 2], 
  #                 [4, 4, 6, 5, 0, 0] ]
  # nr_bins = 8
  # histogram = computeCumulativeHistogram(pixel_array, image_width, image_height, nr_bins)
  # print(histogram)

  # image_width = 6
  # image_height = 5
  # pixel_array = [ [6, 3, 2, 6, 4, 7],
  #               [5, 3, 2, 7, 0, 6],
  #               [6, 2, 7, 7, 1, 7],
  #               [7, 6, 6, 2, 7, 3],
  #               [2, 2, 2, 5, 1, 2] ]
  # nr_bins = 8
  # histogram = computeCumulativeHistogram(pixel_array, image_width, image_height, nr_bins)
  # print(histogram)

  #Q3
  # image_width = 3
  # image_height = 2
  # pixel_array_r = [ [57, 127, 19], [33, 74, 166] ]
  # pixel_array_g = [ [12, 0, 255], [78, 16, 51] ]
  # pixel_array_b = [ [92, 20, 4], [18, 15, 164] ]
  # greyscale_pixel_array = computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height)
  # print(greyscale_pixel_array)

  # Q4
  image_width = 3
  image_height = 2
  pixel_array = [ [57, 127, 19], [33, 74, 166] ]
  contrast_stretched_pixel_array = scaleTo0And255AndQuantize(pixel_array, image_width, image_height)
  print(contrast_stretched_pixel_array)

  image_width = 3
  image_height = 2
  pixel_array = [ [78, 16, 51], [12, 0, 255] ]
  contrast_stretched_pixel_array = scaleTo0And255AndQuantize(pixel_array, image_width, image_height)
  print(contrast_stretched_pixel_array)

  image_width = 2
  image_height = 2
  pixel_array = [ [1, 1], [1, 1] ]
  contrast_stretched_pixel_array = scaleTo0And255AndQuantize(pixel_array, image_width, image_height)
  print(contrast_stretched_pixel_array)