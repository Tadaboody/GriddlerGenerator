import cv2
import numpy as np
from matplotlib import pyplot


def normalize_array(array):
    my_sum = sum(float(element) for row in array for element in row)
    return [[element / my_sum for element in row] for row in array]


def file_name(name):
    return "pics/" + name.replace(".jpg", "a") + '.jpg'


def griddler_count(image):
    resultX = griddler_list(image)
    resultY = griddler_list(np.transpose(image))
    return resultX, resultY


def griddler_list(image):
    image_size = len(image)
    result = [[] for x in range(image_size)]
    segment = False
    for i in range(image_size):
        segment = False
        for j in range(len(image[0])):
            if not image[i][j]:
                if not segment:
                    result[i].append(0)
                    segment = True
                result[i][-1] += 1
            else:
                segment = False
    print(result)
    return result


def resize_maintaining_ratio(image, new_height):
    ratio = float(new_height) / float(len(image))
    new_width = int(len(image[0]) * ratio)
    return cv2.resize(image, (new_width, new_height))


def main():
    image_name = "awoo"

    pyplot.subplot(141)
    image = cv2.imread(file_name(image_name), 0)
    pyplot.imshow(image, "gray")
    pyplot.title(image_name)

    print(image)
    threshold = 180
    ret, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    filter0 = [1] * 2
    ker = [filter0 for i in range(len(filter0))]
    kernel = np.array(ker)
    image = cv2.filter2D(image, -1, kernel)
    print(image)
    pyplot.subplot(142)
    pyplot.title("Threshold:{}".format(threshold))
    pyplot.imshow(image, "gray")
    height, width = (30, 30)
    imagea = resize_maintaining_ratio(image, height)
    # print(image)
    pyplot.subplot(143), pyplot.title("Trunc with ratio:{} by {}".format(height, len(imagea[0]))), pyplot.imshow(imagea,
                                                                                                                 "gray")
    imageb = cv2.resize(image, (width, height))
    pyplot.subplot(144), pyplot.title("Trunc:{} by {}".format(height, width)), pyplot.imshow(imageb, "gray")
    # def jpeg_trunc(size):
    #     while True:
    #         try:
    print(griddler_count(imagea))
    print(griddler_count(imagea)[1])
    pyplot.show()


if __name__ == "__main__":
    main()


def blur_by(image, value, core=2):
    if int(value):
        filter0 = [1] * int(value)
        filter0[int(value) // 2] = core
        ker = normalize_array([filter0 for i in range(len(filter0))])
        kernel = np.array(ker)
        image = cv2.filter2D(image, -1, kernel)
    return image
