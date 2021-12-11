import numpy as np
import matplotlib.pyplot as plt

import cv2 as cv

#chr https://www.kite.com/python/answers/how-to-convert-an-int-to-ascii-and-back-in-python
#https://numpy.org/doc/stable/reference/random/generated/numpy.random.laplace.html

def gen_normal(size, loc=0.0, scale=1.0):
    return np.random.normal(loc=loc, scale=scale, size=size)


def gen_laplace(size, loc=0.0, scale=1.0):
    return np.random.laplace(loc=loc, scale=scale, size=size)


def gen_uniform(size, lower=32, upper=127):
    return np.random.uniform(lower, upper + 1, size)


def normalize(data, lower=32, upper=127):
    data = (data - np.min(data)) / (np.max(data) - np.min(data))# [0,1]
    data = (data * (upper - lower)) + lower
    data = np.round(data)
    return data


def convert_to_string(data):
    return "".join([chr(int(num)) for num in data])


def plot_hist(data, plot_name, buckets=100):
    counts, bins = np.histogram(data, bins=buckets)
    plot = plt.hist(bins[:-1], bins=bins, weights=counts)
    plt.title(plot_name)
    plt.savefig("{}.png".format(plot_name))
    plt.show()

    return plot


def write_to_file(file_name, data):
    with open(file_name,"w") as file:
        file.writelines(data)


def read_image(image_path):
   return np.ravel(cv.imread(image_path))


def read_txtfile(file_name):
    file = open(file_name,"r",)
    data = file.read()
    file.close()

    return [ord(k) for k in data]


def plot_histogram(filename):
    data = None
    if filename.endswith(".png") or filename.endswith(".jpg"):
        data = read_image(filename)
        buckets = 256
    elif filename.endswith(".txt"):
        data = read_txtfile(filename)
        buckets = 96
    else:
        print("Not recognised file format. Try: .jpg, .png, .txt")
        return

    plot_name = filename[:len(filename)-4]
    plot_hist(data=data, plot_name=plot_name, buckets=buckets)



"""
d1 = gen_uniform(1024 *8)
d2 = convert_to_string(normalize(d1,33))
write_to_file("example.txt", d2)

plot_histogram("example.txt")

d1 = gen_normal(1024 *8)
d3 = normalize(d1)
d2 = convert_to_string(normalize(d1,33))
print(type(d2))
write_to_file("example.txt", d2)

data = read_txtfile("example.txt")
print(data)
a = plot_histogram(data,"data1.png")



data = read_image("1.png")
print(len(data))
plot_histogram(data,"data2.png",256)

d1 = gen_normal(10000)
plot_histogram(d1)

d2 = gen_laplace(10000)
plot_histogram(d2)

d1 = gen_normal(10000)
d3 = normalize(d1)
d2 = convert_to_string(normalize(d1,33))
print(d1)
counts, bins = np.histogram(d1,bins=100)
print(counts)
print(bins)
plt.hist(bins[:-1], bins=bins, weights=counts)
plt.show()

counts, bins = np.histogram(d3,bins=100)
plt.hist(bins[:-1], bins=bins, weights=counts)
plt.show()

"""