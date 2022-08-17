######################################################################
# File: image_masking.py
# Project: Research Project (M.Sc.)
# Created Date: 17.08.2022
# Author: Nico Leuze,
#         Faculty of Electrical Engineering and Information Technology
#         University of Applied Science Munich (MUAS)
# -----
# Last Modified: 17.08.2022
# Modified By: Nico Leuze
# -----
# Copyright (c) 2022 MUAS
######################################################################

import cv2
import numpy as np
import os 
import random

def make_background(org_image, background_image):
    img = org_image
    low_tresh = np.array([200,180,150], dtype=np.uint8)
    high_tresh = np.array([255,255,255], dtype=np.uint8)
    mask = cv2.inRange(img, low_tresh, high_tresh)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    mask = cv2.bitwise_not(mask)

    # load background: White Background
    bk = np.full(img.shape, 255, dtype=np.uint8)

    # foreground mask
    fg_masked = cv2.bitwise_and(img, img, mask=mask)

    # get masked background, mask must be inverted 
    mask = cv2.bitwise_not(mask)
    bk_masked = cv2.bitwise_and(bk, bk, mask=mask)
    
    # combine masked foreground and masked background 
    final = cv2.bitwise_or(fg_masked, bk_masked)
    # cv2.imwrite('bkg_img.png', final)
    mask = cv2.bitwise_not(mask)  # revert mask to original

    #
    ########################
    #

    # Adding Background:
    low_tresh = np.array([255,255,255], dtype=np.uint8)
    high_tresh = np.array([255,255,255], dtype=np.uint8)
    mask = cv2.inRange(final, low_tresh, high_tresh)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    mask = cv2.bitwise_not(mask)
    # print('Maske: ', type(mask), mask.shape)
    # cv2.imshow(winname='mask', mat=mask)
    # cv2.waitKey(10000)

    # load background: Randomly chosen background image
    bkg_img = background_image

    # get masked foreground
    fg_masked = cv2.bitwise_and(final, final, mask=mask)

    # get masked background, mask must be inverted 
    mask = cv2.bitwise_not(mask)
    bk_masked = cv2.bitwise_and(bkg_img, bkg_img, mask=mask)

    # combine masked foreground and masked background 
    final = cv2.bitwise_or(fg_masked, bk_masked)
    # cv2.imwrite('bkg_img_final.png', final)
    return final

def main():
    syn_image_base_folder = './example_images/masking_org/'
    bkg_image_folder = './example_images/masking_bkg/'
    
    for syn_image_folder, dirs, files in os.walk(syn_image_base_folder):
        print(syn_image_folder)
        # for img_name in os.listdir(root):
        #     if img_name.endswith('png'):
        #         print(img_name)

        for img_name in os.listdir(syn_image_folder):
            if img_name.endswith('png'):
                print(img_name)
                img_path = syn_image_folder + '/' + img_name
                print(img_path)
                img = cv2.imread(img_path)
                bkg_img_name = random.choice(os.listdir(bkg_image_folder))
                bkg_img_path = bkg_image_folder + bkg_img_name
                bkg_img = cv2.imread(bkg_img_path)
                
                mod_img = make_background(img, bkg_img)
                cv2.imwrite(img_path, mod_img)

if __name__ == '__main__':
    main()