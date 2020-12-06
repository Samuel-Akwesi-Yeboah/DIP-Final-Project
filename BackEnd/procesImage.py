import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

def build_keypoint_descriptor_library(file_names,sift):
    keypoints = list()
    descriptors = list()
    i = 0
    for file in file_names:
        img = cv.imread(os.getcwd() +"/trainingImages/" +  file)
        gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        keypoints_1, descriptors_1 = sift.detectAndCompute(gray_img,None)
        #keypoint_map = cv.drawKeypoints(gray_img,keypoints_1,img,color=red_color)
        keypoints.append(keypoints_1)
        descriptors.append(descriptors_1)
    return keypoints,descriptors

def test_image(file_path):
    #matplotlib inline
    #Read image
    file_name  = 'training_image_'
    file_ending = '.jpg'
    sift = cv.SIFT_create(3000)
    file_names = list()
    for i in range(1,6):
        file1 = file_name + str(i) + file_ending
        file_names.append(file1)

    keypoint_list,descriptor_list = build_keypoint_descriptor_library(file_names,sift)

    sift = cv.SIFT_create(5000)
    test_image = cv.imread(os.getcwd() + "/static/" + file_path)
    test_image_gray = cv.imread(os.getcwd() + "/static/" + file_path,cv.IMREAD_GRAYSCALE)
    test_image_keypoints,test_image_descriptors = sift.detectAndCompute(test_image_gray,None)
    #keypoint_map = cv.drawKeypoints(test_image_gray,test_image_keypoints,test_image,color=red_color)
    #file_path = './keypoint_maps/keypoint_map_test_image_4' + '.jpg'

    brute_matcher =  cv.BFMatcher()
    temp = int(2)

    for i in range(len(descriptor_list)):
        training_image = cv.imread(os.getcwd() +"/trainingImages/" +  file_names[i])
        print(training_image)
        descriptor = descriptor_list[i]
        keypoint = keypoint_list[i]
        matches = brute_matcher.knnMatch(descriptor,test_image_descriptors,k=temp)
        good = []
        good_matches_list = []
        for m,n in matches:
            if  m.distance < .6 * n.distance:
                good.append(m)
                good_matches_list.append([m]) 

        failed_comparison = 0
        #Not enough keypoints. The lime is illegally parked or cannot be checked
        if len(good) != 0:

            print("The lime is present in the picture")

            src_pts = np.float32([keypoint[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dst_pts = np.float32([test_image_keypoints[m.trainIdx].pt for m in good]).reshape(-1,1,2)

            M, mask = cv.findHomography(src_pts,dst_pts,cv.RANSAC,float(5.0))
            matches_mask = mask.ravel().tolist()

            h,w,l = training_image.shape
            pts = np.float32([[0,0] , [0,h-1] , [w-1,h-1], [w-1,0] ]).reshape(-1 ,1 ,2)
            dst = ''
            if M:
                dst = cv.perspectiveTransform(pts,M)
                mappedImage = cv.polylines(test_image, [np.int32(dst)], True, 255, 3, cv.LINE_AA)
            else:
                return "The Lime was parked incorrectly"
        else:
            failed_comparison +=1

    if failed_comparison == len(file_names):
        return "The Lime is parked incorrectly"
    return "The lime was parked correctly"
