import numpy as np
import cv2
import glob
from scipy.spatial import distance
import pandas as pd
import os

class Iris_Recognition:
    
    def localize_iris(self,image):
        #reading image
        img = cv2.imread(image,0)
        #resizing image
        img = cv2.resize(img, (800,600))
        #converting image to grayscale
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        #applying blur
        img = cv2.GaussianBlur(img, (5,5), 0)
        #creating mask
        _, threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #detectig edges
        canny = cv2.Canny(threshold, 40,50) 
        #finding circles in edges
        circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 1, canny.shape[0]/1, param1=70, param2=30, minRadius=0, maxRadius=400)
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            #cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            #cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
            x = i[0] - 160
            y = i[1] - 160
            crop = cimg[y:y + 320, x:x + 320]
            r = i[2]
        # cv2.imshow('threshold',threshold)
        # cv2.imshow('original',cimg)
        # cv2.imshow('edges',canny)
        # cv2.imshow('crop', crop)
        return (crop,r)


    def normalize_iris(self,image, height, width, r_in, r_out):       
        thetas = np.arange(0, 2 * np.pi, 2 * np.pi / width)  # Theta values
        r_out = r_in + r_out
        # Create empty flatten image
        flat = np.zeros((height,width, 3), np.uint8)
        circle_x = int(image.shape[0] / 2)
        circle_y = int(image.shape[1] / 2)

        for i in range(width):
            for j in range(height):
                theta = thetas[i]  # value of theta coordinate
                r_pro = j / height  # value of r coordinate(normalized)

                # get coordinate of boundaries
                Xi = circle_x + r_in * np.cos(theta)
                Yi = circle_y + r_in * np.sin(theta)
                Xo = circle_x + r_out * np.cos(theta)
                Yo = circle_y + r_out * np.sin(theta)

                # the matched cartesian coordinates for the polar coordinates
                Xc = (1 - r_pro) * Xi + r_pro * Xo
                Yc = (1 - r_pro) * Yi + r_pro * Yo
                
                color = image[int(Xc/2)][int(Yc/2)]  # color of the pixel

                flat[j][i] = color
        return flat

    def encode_features(self,image):
        g_kernel = cv2.getGaborKernel((27, 27), 8.0, np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)
        filtered_img = cv2.filter2D(image, cv2.CV_8UC3, g_kernel)
        h, w = g_kernel.shape[:2]
        g_kernel = cv2.resize(g_kernel, (3*w, 3*h), interpolation=cv2.INTER_CUBIC)
        return filtered_img
    
    def match_iris(self,iris,irisList):
        check = False
        img = ''
        for i in irisList:
            if distance.hamming(iris.ravel(),i.ravel()) == 0:
                check = True
                img = i.ravel()
                break
        return (check, img)

    # image_path = '/home/akramnarejo/Downloads/azmat/project/images/020/IMG_020_L_2.JPG'
    # crop,r = localize_iris(image_path)
    # image_nor = normalize_iris(crop, 60, 300, r, 100)
    # encode_features(image_nor)


    # dist = distance.hamming(filtered_img.ravel(), data[i].ravel())




    # print(type(filtered_img.ravel()))
    # #print(features)
    #cv2.imshow('filter',filtered_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
