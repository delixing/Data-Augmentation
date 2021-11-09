import numpy as np
from PIL import Image
import random
import os

#--------------------------------------#
#   according to the paper 
#   "Augmentation for small object dection"
#   https://arxiv.org/pdf/1912.06319.pdf
#   the oversampling rate should be 3 times
#--------------------------------------#

#--------------------------------------#
# filter for the file, only .jpg file
#--------------------------------------#
def file_filter(f):
    if f[-4:] in ['.jpg']:
        return True
    else:
        return False
#--------------------------------------#
# from xc yc w h, to x y x y, left-top to right-bottom
#--------------------------------------#
def convert(img_width, img_height, box):
    x_min = (float(box[1]) - float(box[3])/2.0)*img_width
    y_min = (float(box[2]) - float(box[4])/2.0)*img_height
    x_max = (float(box[1]) + float(box[3])/2.0)*img_width
    y_max = (float(box[2]) + float(box[4])/2.0)*img_height
    return (int(x_min),int(y_min),int(x_max),int(y_max))
#--------------------------------------#
# from x y x y, left-top to right-bottom to xc yc w h
#--------------------------------------#
def convert_2yolo(img_width, img_height, box):
    x_center = ((float(box[2]) + float(box[0]))/2.0)/img_width
    y_center = ((float(box[3]) + float(box[1]))/2.0)/img_height
    x_width = (float(box[2]) - float(box[0]))/img_width
    y_height = (float(box[3]) - float(box[1]))/img_height
    return (x_center,y_center,x_width,y_height)

def get_box(annotation_path, img_width, img_height):
    with open(annotation_path) as f:
        box_list = []
        classes_list = []
        for line in f.readlines():
            line = line.split(' ')
            box = convert(img_width,img_height,line)
            box_list.append(box)
            classes_list.append(int(line[0]))
    return box_list,classes_list

def crop_from_img(images,rd):
    img_seed_1 = random.choice(images)
    img_seed_2 = random.choice(images)
    img_seed_3 = random.choice(images)
    img_1 = Image.open(rd+img_seed_1)
    img_w_1, img_h_1 = img_1.size
    img_2 = Image.open(rd+img_seed_2)
    img_w_2, img_h_2 = img_2.size
    img_3 = Image.open(rd+img_seed_3)
    img_w_3, img_h_3 = img_3.size

    annotation_1 = rd+img_seed_1[:-3]+'txt'
    annotation_2 = rd+img_seed_2[:-3]+'txt'
    annotation_3 = rd+img_seed_3[:-3]+'txt'
    seed_box_list_1, seed_classes_list_1 = get_box(annotation_1,img_w_1,img_h_1)
    seed_box_list_2, seed_classes_list_2 = get_box(annotation_2,img_w_2,img_h_2)
    seed_box_list_3, seed_classes_list_3 = get_box(annotation_3,img_w_3,img_h_3)
    all_boxes=[]
    all_classes=[]
    all_patches=[]
    for index,box in enumerate(seed_box_list_1):
        img_patch_1 = img_1.crop(box)
        all_boxes.append(box)
        all_classes.append(seed_classes_list_1[index])
        all_patches.append(img_patch_1)
    for index,box in enumerate(seed_box_list_2):
        img_patch_2 = img_2.crop(box)
        all_boxes.append(box)
        all_classes.append(seed_classes_list_2[index])
        all_patches.append(img_patch_2)
    for index,box in enumerate(seed_box_list_3):
        img_patch_3 = img_3.crop(box)
        all_boxes.append(box)
        all_classes.append(seed_classes_list_3[index])
        all_patches.append(img_patch_3)
    return all_boxes,all_classes,all_patches

def ifinbox(x,y,boxes):
    for index,box in enumerate(boxes):
        if box[0]<x<box[2] and box[1]<y<box[3]:
            return True
    return False   


def implement_copy_paste(images,rd,save_path):
    np.random.shuffle(images)
    for image in images:
        img = Image.open(rd+image)
        img_w, img_h = img.size
        root_box_list,root_classes_list = get_box(rd+image[:-3]+'txt',img_w,img_h)
        seed_boxes,seed_classes,seed_patches = crop_from_img(images,rd)
        annotation = ''
        paste_boxes = []
        for index,seed_patch in enumerate(seed_patches):
            scale = np.random.rand(2)
            x_position = int(img_w*scale[0])
            y_position = int(img_h*scale[1])
            inbox = ifinbox(x_position,y_position,root_box_list)
            #-----------------------------#
            #   avoid cover the original box
            #-----------------------------#
            while inbox:
                scale = np.random.rand(2)
                x_position = int(img_w*scale[0])
                y_position = int(img_h*scale[1])
            patch_width = seed_boxes[index][2]-seed_boxes[index][0]
            patch_height = seed_boxes[index][3]-seed_boxes[index][1]
            paste_box = (x_position,y_position,x_position+patch_width,y_position+patch_height)
            paste_boxes.append(paste_box)
            img.paste(seed_patch, paste_box)
        all_boxes = paste_boxes+root_box_list
        all_classes = seed_classes+root_classes_list
        img_path = save_path+ image[:-4]+'copy'+'.jpg'
        img.save(img_path)
        for index,all_box in enumerate(all_boxes):
            x_center,y_center,x_width,y_height = convert_2yolo(img_w, img_h, all_box)
            annotation = annotation+str(all_classes[index])+' '+(' ').join([str(x_center),str(y_center),str(x_width),str(y_height)])+'\n'
            txt_path = img_path[:-3]+'txt'
            with open(txt_path,'w') as f:
                f.write(annotation)
'''
if __name__ == '__main__':
    np.random.seed(100000)
    rd = 'test/'
    paths = os.listdir(rd)
    images = list(filter(file_filter, paths))
    save_path = 'save/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    implement_copy_paste(images,rd,save_path)
'''

