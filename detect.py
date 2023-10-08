import cv2
import numpy as np
import random as rng
import json

im = cv2.imread("ngc13big.png")

cv2.imshow('src', im)

kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
imgLaplacian = cv2.filter2D(im, cv2.CV_32F, kernel)
sharp = np.float32(im)
imgResult = sharp - imgLaplacian
imgResult = np.clip(imgResult, 0, 255)
imgResult = imgResult.astype('uint8')
imgLaplacian = np.clip(imgLaplacian, 0, 255)
imgLaplacian = np.uint8(imgLaplacian)

# cv2.imshow('sharp', imgResult)

im_bw = cv2.cvtColor(imgResult, cv2.COLOR_BGRA2GRAY)

im_blur = np.zeros(im_bw.size)

im_blur = cv2.GaussianBlur(im_bw, (0,0) ,1, im_blur)

im_equalized = cv2.equalizeHist(im_blur);

otsu_tr, im_thresh = cv2.threshold(im_equalized, 200, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

dist = cv2.distanceTransform(im_thresh, cv2.DIST_L2, 0);

cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)

_, dist = cv2.threshold(dist, 0.2, 1.0, cv2.THRESH_BINARY)

kernel1 = np.ones((3,3), dtype=np.uint8)
dist = cv2.dilate(dist, kernel1)

dist_8u = dist.astype('uint8')
# Find total markers
contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

objects = {}

for i in range(len(contours)):
    x,y,w,h = cv2.boundingRect(contours[i])
    objects[i] = {"x": x, "y": y, "w": w, "h":h}
    im_crop = im[y:y+h, x:x+w]
    im_crop = cv2.cvtColor(im_crop, cv2.COLOR_BGR2BGRA)
    mask = np.zeros((im.shape[0] , im.shape[1]), np.uint8)
    cv2.drawContours(mask, contours, i, (255), -1)
    
    mask_crop = mask[y:y+h, x:x+w]

    print(im_crop.shape)
    print(mask_crop.shape)

    im_masked = cv2.bitwise_and(im_crop, im_crop, mask=mask_crop)

    cv2.imwrite("objects/object{}.png".format(i), im_masked)

with open('objects.json', 'w') as f:
    json.dump(objects, f)

# Create the marker image for the watershed algorithm

markers = np.zeros(dist.shape, dtype=np.int32)

for i in range(len(contours)):
    cv2.drawContours(markers, contours, i, (i+1), -1)

# Draw the background marker
cv2.circle(markers, (5,5), 3, (255,255,255), -1)

markers_8u = (markers * 10).astype('uint8')
cv2.imshow('Markers', markers_8u)

#cv2.watershed(imgResult, markers)

#cv2.imshow('Distance Transform Image', dist)

#mark = markers.astype('uint8')
#mark = cv2.bitwise_not(mark)
#colors = []
#for contour in contours:
# colors.append((rng.randint(0,256), rng.randint(0,256), rng.randint(0,256)))

#dst = np.zeros((markers.shape[0], markers.shape[1], 3), dtype=np.uint8)

#for i in range(markers.shape[0]):
# for j in range(markers.shape[1]):
#    index = markers[i,j]
#    if index > 0 and index <= len(contours):
#        dst[i,j,:] = colors[index-1]
# Visualize the final image
#cv2.imshow('Final Result', dst)

cv2.waitKey(0)
