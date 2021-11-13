from copy_paste_with_rotation import implement_copy_paste,file_filter
import os
import numpy as np

if __name__ == '__main__':
    np.random.seed(100000)
    rd = 'test/'
    paths = os.listdir(rd)
    images = list(filter(file_filter, paths))
    save_path = 'save/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    implement_copy_paste(images,rd,save_path)