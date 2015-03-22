import cv2
import numpy as np
import sys

# this script will find lines and circles in an image

# constrained to find medium-sized circles (for bike wheels)
# and near-vertical lines for identifying buses

# to invoke:
# python /path/to/hough_opencv.py /path/to/input_image.jpg

# there are several python packages that need to be installed
# follow instructions in
# http://docs.opencv.org/doc/tutorials/introduction/windows_install/windows_install.html

# code adapted from
# http://www.janeriksolem.net/2012/08/reading-gauges-detecting-lines-and.html

# load grayscale image
im = cv2.imread(sys.argv[1])
gray_im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

# create version to draw on and blurred version
draw_im = cv2.cvtColor(gray_im, cv2.COLOR_GRAY2BGR)
blur = cv2.GaussianBlur(gray_im, (0,0), 5)

m,n = gray_im.shape

# Hough transform for circles
circles = cv2.HoughCircles(gray_im, cv2.cv.CV_HOUGH_GRADIENT, .25, 150,
        np.array([]), 40, 20, minRadius=50,maxRadius=200)[0]


# Hough transform for lines (regular and probabilistic)
edges = cv2.Canny(blur, 20, 60)
lines = cv2.HoughLines(edges, 2, np.pi/90, 40)[0]
plines = cv2.HoughLinesP(edges, 1, np.pi/180, 20, np.array([]), 10, 400)[0]


# draw
for c in circles[:25]:
    # green for circles
    cv2.circle(draw_im, (c[0],c[1]), c[2], (0,255,0), 2)


for (rho, theta) in lines[:500]:
    # blue for infinite lines
    boundary = 5 * np.pi / 180 # only vertical lines (+/- 5 degrees)

    if theta > boundary and theta < ( np.pi - boundary ):
        continue
    x0 = np.cos(theta)*rho
    y0 = np.sin(theta)*rho
    pt1 = ( int(x0 + (m+n)*(-np.sin(theta))), int(y0 + (m+n)*np.cos(theta)) )
    pt2 = ( int(x0 - (m+n)*(-np.sin(theta))), int(y0 - (m+n)*np.cos(theta)) )
    cv2.line(draw_im, pt1, pt2, (255,0,0), 2)

for l in plines[:25]:
    # red for line segments
    cv2.line(draw_im, (l[0],l[1]), (l[2],l[3]), (0,0,255), 2)

cv2.imshow("output",draw_im)
cv2.waitKey()

# save the resulting image
cv2.imwrite("output.jpg",draw_im)
