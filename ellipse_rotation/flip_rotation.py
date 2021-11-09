import cv2
import imutils
from ellipse import ellipserotate



def getRotatedImg(angle, img_path, img_write_path, outpath_re, txt_path):
    img = cv2.imread(img_path)
    rotation_image = imutils.rotate_bound(img,angle)

    cv2.imwrite(img_write_path, rotation_image)
    height,width = img.shape[:2]
    height_new,width_new = rotation_image.shape[:2]

    with open(txt_path,'r') as f:
        ann_re = ''
        for line in f.readlines():
            line = line.split(' ')
            x_c = float(line[1])*width
            y_c = float(line[2])*height
            b_W = float(line[3])*width
            b_H = float(line[4])*height
            
            pointx = width/2
            pointy = height/2
    
            x_min,y_min,x_max,y_max = ellipserotate(-angle,b_H,b_W,x_c,y_c,pointx,pointy)
            x_min = x_min + (width_new-width)/2
            x_max = x_max + (width_new-width)/2
            y_min = y_min + (height_new-height)/2
            y_max = y_max + (height_new-height)/2

            x_c_ = float(((x_min + x_max)/2)/width_new)
            y_c_ = float(((y_min + y_max)/2)/height_new)
            b_W_ = float((x_max - x_min)/width_new)
            b_H_ = float((y_max - y_min)/height_new)
            ann_re = ann_re + line[0] + ' ' + str(x_c_) + ' ' + str(y_c_) + ' ' + str(b_W_) + ' ' + str(b_H_) + '\n'
            with open(outpath_re, 'w') as outfile:
                outfile.write(ann_re)
'''
if __name__ == '__main__':
    angle = 25
    img_path = "C:/Users/Frank/Desktop/DA/ellipse_rotation/test/0000122_01200_d_0000119.jpg"
    img_write_path = 'C:/Users/Frank/Desktop/DA/ellipse_rotation/test/0.jpg'
    outpath_re = "C:/Users/Frank/Desktop/DA/ellipse_rotation/test/0.txt"
    txt_path = "C:/Users/Frank/Desktop/DA/ellipse_rotation/test/0000122_01200_d_0000119.txt"

    getRotatedImg(angle, img_path, img_write_path, outpath_re, txt_path)
'''