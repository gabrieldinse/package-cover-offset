# Author: Felipe Alfredo Nack
# File: TemplateMatching
# Date: 03/11/2020


import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('pc2.JPEG', 0)
img2 = img.copy()
template = cv2.imread('template.jpg', 0)
#h, w, dim = template.shape

# All the 6 methods for comparison in a list
methods = ['cv2.TM_SQDIFF_NORMED']

found = None

for meth in methods:
    for scale in np.linspace(0.8, 1.2, 9):
        i = 1
        for i in [1,2]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(template, width=int(template.shape[1] * scale))
            r = template.shape[1] / float(resized.shape[1])
            h, w = resized.shape
            if i == 2:
                center = (w/2, h/2)
                M = cv2.getRotationMatrix2D(center, 180, 1.0)
                resized = cv2.warpAffine(resized, M, (h, w))

            #r = template.shape[1] / float(resized.shape[1])
            # if the resized image is smaller than the template, then break
            # from the loop
            #if resized.shape[0] < tH or resized.shape[1] < tW:
            #    break

            img = img2.copy()
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(img,resized,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print(min_val, max_val, min_loc, max_loc)

            if found is None or min_val < found[0]:
                found = (min_val, min_loc, scale, max_loc)


            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            # #
            cv2.rectangle(img,top_left, bottom_right, 255, 2)
            # #
            res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # #
            plt.subplot(121),plt.imshow(res, cmap='gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(img)
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)
            #
            plt.show()


# bottom_right = (found[1][0] + w, found[1][1] + h)
# cv2.rectangle(img,found[1], bottom_right, 255, 2)
# res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.subplot(121),plt.imshow(res, cmap='gray')
# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(img)
# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
# plt.suptitle(meth)
print(found)
h, w = template.shape
centroide = (found[1][0] + found[2]*w/2, found[1][1] + found[2]*h/2)
print(centroide)
# plt.show()
