# Procedural Terrain Generation with Thermal Erosion

import matplotlib
import itertools
import noise
import numpy as np
import PIL.Image
from io import StringIO
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from random import randint
from math import hypot

def heightmap_from_image(filename):
    im = PIL.Image.open(filename)
    pixels = np.asarray(im)
    width, height = im.size
    heightmap = np.zeros((width,height))
    for x in range(width):
        for y in range(height):
            heightmap[x][y] = pixels[x][y]
    return heightmap
# plots a heightmap using matplotlib
def plot_heightmap(heightmap,title):
    mapsize = len(heightmap)
    x = [i for i in range(mapsize)]
    y = [i for i in range(mapsize)]
    x, y = np.meshgrid(x,y)
    fig = plt.figure(figsize=(10,4))
    ax = Axes3D(fig)
    #ax.plot_surface(x, y, heightmap, cmap=plt.cm.coolwarm, rcount=255, ccount=255)
    ax.plot_surface(x, y, heightmap, cmap=plt.cm.coolwarm, rcount=25, ccount=25, antialiased=False)
    plt.title(title)
    plt.axis([0,mapsize,0,mapsize])
#converts a heightmap to a b&w image and displays it
def display_image(heightmap):
    PIL.Image.fromarray(heightmap).show()
# saves the b&w image of the heightmap as a png
def save_image(heightmap,filename):
    PIL.Image.fromarray(heightmap).convert("L").save(filename,"PNG")

# Generates a 2d array heightmap using either Perlin noise or Worley noise
def generate_heightmap(mapsize, method):
    heightmap = np.zeros((mapsize, mapsize))
    if (method == "perlin"):
        offset = randint(0,(mapsize - 1))
        print("Generating Perlin Terrain...")
        for x in range(mapsize):
            for y in range(mapsize):
                heightmap[x][y] = noise.snoise2(x/(mapsize-1) + offset, y/(mapsize-1) + offset, octaves=4) * 128 + 128
    if (method == "worley"):
        print("Generating Worley Terrain...")
        NUM_PTS = 50
        N = 0
        wp_ys = np.zeros((NUM_PTS))
        wp_xs = np.zeros((NUM_PTS))
        for i in range(NUM_PTS):
            wp_ys[i] = randint(0, (mapsize-1))
            wp_xs[i] = randint(0, (mapsize-1))
        for x in range(mapsize):
            for y in range(mapsize):
                distances = [hypot(wp_xs[i] - x, wp_ys[i] - y) for i in range(NUM_PTS)]
                distances.sort()
                heightmap[x][y] = (mapsize-1) - (2 * (mapsize-1) * distances[N] / distances[-1] + (mapsize-1)/1.25 * distances[N+1]/distances[-1] + (mapsize-1)/1.5 * distances[N+2]/distances[-1]+ (mapsize-1)/1.75 * distances[N+3]/distances[-1])
    print("Complete!")
    return heightmap


def get_neighbors(heightmap, x,y):
    mapsize = len(heightmap)
    neighbors = []
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if ( np.abs(x + dx) < mapsize and np.abs(y + dy) < mapsize):
                neighbors.append((x+ dx, y + dy))
    return neighbors

### defines the thermal erosion method documented by https://web.mit.edu/cesium/Public/terrain.pdf
def therm_erode(heightmap, iterations):
    mapsize = len(heightmap) 
    TALUS = 4/mapsize
    copymap = [row[:] for row in heightmap]
    for it in range(iterations):
        print(it + 1,"/",iterations)
        for y in range(mapsize):
            for x in range(mapsize):
                h = heightmap[x][y]
                neighbors = get_neighbors(heightmap, x, y)
                neighbor_deltas = []
                for point in neighbors:
                    neighbor_deltas.append(h - heightmap[point[0]][point[1]])
                dmax = max(neighbor_deltas)
                index_of_increase = neighbor_deltas.index(dmax)
                if (dmax <= TALUS):
                    continue

                dmax *= .25
                heightmap[x][y] -= dmax
                heightmap[neighbors[index_of_increase][0]][neighbors[index_of_increase][1]] += dmax



terrain = generate_heightmap(256,"worley")
save_image(terrain, "initial.png")
therm_erode(terrain,1)
save_image(terrain,"final.png")
