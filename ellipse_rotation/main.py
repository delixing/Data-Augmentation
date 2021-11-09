from flip_rotation import getRotatedImg
import random
import os

rd = 'C:/Users/Frank/Desktop/test/'
rd_new = 'C:/Users/Frank/Desktop/new/'
imgs = os.listdir('C:/Users/Frank/Desktop/test/')

for img in imgs:
    if img[-3:] != 'jpg':
        continue
    img_path = rd + img
    probab = random.random()
    if probab > 0.0:
                
        img_write_path_ro = rd_new + 'ag_' + img[:-4] + '_ro.jpg'
        #angle = (abs(random.gauss(0, 1))/2)*50
        angle = 45
        outpath_re = rd_new + 'ag_' + img[:-4] + '_ro.txt'
        txt_path = rd + img[:-4] + '.txt'
        getRotatedImg(angle, img_path, img_write_path_ro, outpath_re, txt_path)
    