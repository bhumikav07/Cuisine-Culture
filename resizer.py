import os
import cv2

for images in os.listdir('static/images'):
    img = cv2.imread('static/images/'+images, cv2.IMREAD_UNCHANGED)
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite('static/images/'+images, resized)